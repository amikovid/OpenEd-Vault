import { NextRequest, NextResponse } from "next/server";
import { promises as fs } from "fs";
import path from "path";

const HUBSPOT_ACCESS_TOKEN = process.env.HUBSPOT_API_KEY;

// Fallback: save to local JSON file when HubSpot isn't configured/working
async function saveToLocalFile(data: Record<string, unknown>) {
  try {
    const filePath = path.join(process.cwd(), "captured-emails.json");
    let existing: Record<string, unknown>[] = [];

    try {
      const content = await fs.readFile(filePath, "utf-8");
      existing = JSON.parse(content);
    } catch {
      // File doesn't exist yet
    }

    existing.push({
      ...data,
      capturedAt: new Date().toISOString(),
    });

    await fs.writeFile(filePath, JSON.stringify(existing, null, 2));
    console.log("Email saved to captured-emails.json");
    return true;
  } catch (err) {
    console.error("Failed to save to local file:", err);
    return false;
  }
}

interface HubSpotContactInput {
  email: string;
  state?: string;
  primaryPhilosophy: string;
  primaryPhilosophyName: string;
  secondaryPhilosophies?: string[];
  confidence?: number;
}

export async function POST(request: NextRequest) {
  let capturedData: HubSpotContactInput | null = null;

  try {
    const body: HubSpotContactInput = await request.json();
    capturedData = body;
    const { email, state, primaryPhilosophy, primaryPhilosophyName, secondaryPhilosophies, confidence } = body;

    if (!email) {
      return NextResponse.json({ error: "Email is required" }, { status: 400 });
    }

    if (!HUBSPOT_ACCESS_TOKEN) {
      console.warn("HUBSPOT_API_KEY not configured - saving to local file");
      await saveToLocalFile({ email, state, primaryPhilosophy, primaryPhilosophyName, secondaryPhilosophies, confidence });
      return NextResponse.json({
        success: true,
        message: "Email captured (saved locally)",
        contactId: null
      });
    }

    // Create or update contact in HubSpot
    const hubspotResponse = await fetch(
      "https://api.hubapi.com/crm/v3/objects/contacts",
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${HUBSPOT_ACCESS_TOKEN}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          properties: {
            email,
            state: state || "",
            curriculove_primary_philosophy: primaryPhilosophy,
            curriculove_philosophy_name: primaryPhilosophyName,
            curriculove_secondary_philosophies: secondaryPhilosophies?.join(", ") || "",
            curriculove_confidence: confidence?.toString() || "",
            curriculove_quiz_date: new Date().toISOString().split("T")[0],
            lifecyclestage: "lead",
            hs_lead_status: "NEW",
          },
        }),
      }
    );

    // Handle "contact already exists" case
    if (hubspotResponse.status === 409) {
      // Contact exists - update instead
      const existingData = await hubspotResponse.json();
      const existingId = existingData.message?.match(/Existing ID: (\d+)/)?.[1];

      if (existingId) {
        const updateResponse = await fetch(
          `https://api.hubapi.com/crm/v3/objects/contacts/${existingId}`,
          {
            method: "PATCH",
            headers: {
              "Authorization": `Bearer ${HUBSPOT_ACCESS_TOKEN}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              properties: {
                state: state || "",
                curriculove_primary_philosophy: primaryPhilosophy,
                curriculove_philosophy_name: primaryPhilosophyName,
                curriculove_secondary_philosophies: secondaryPhilosophies?.join(", ") || "",
                curriculove_confidence: confidence?.toString() || "",
                curriculove_quiz_date: new Date().toISOString().split("T")[0],
              },
            }),
          }
        );

        if (updateResponse.ok) {
          return NextResponse.json({
            success: true,
            contactId: existingId,
            updated: true
          });
        }
      }
    }

    if (!hubspotResponse.ok) {
      const errorData = await hubspotResponse.json();
      console.error("HubSpot error:", errorData);

      // Save to local file as fallback
      await saveToLocalFile({ email, state, primaryPhilosophy, primaryPhilosophyName, secondaryPhilosophies, confidence });

      return NextResponse.json({
        success: true,
        message: "Email captured (saved locally, HubSpot sync pending)",
        error: errorData.message
      });
    }

    const contactData = await hubspotResponse.json();

    return NextResponse.json({
      success: true,
      contactId: contactData.id
    });

  } catch (error) {
    console.error("HubSpot API error:", error);

    // Save to local file as fallback
    if (capturedData) {
      await saveToLocalFile(capturedData as unknown as Record<string, unknown>);
    }

    return NextResponse.json({
      success: true,
      message: "Email captured (saved locally)",
      error: String(error)
    });
  }
}
