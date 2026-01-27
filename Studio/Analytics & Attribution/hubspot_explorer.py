#!/usr/bin/env python3
"""
HubSpot Data Explorer
Surveys available data: properties, forms, lists, and sample contacts
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Load API key from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
API_KEY = None

with open(env_path) as f:
    for line in f:
        if line.startswith("HUBSPOT_API_KEY="):
            API_KEY = line.strip().split("=", 1)[1]
            break

if not API_KEY:
    print("ERROR: HUBSPOT_API_KEY not found in .env")
    exit(1)

BASE_URL = "https://api.hubapi.com"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def api_get(endpoint, params=None):
    """Make GET request to HubSpot API"""
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {endpoint}")
        print(response.text[:500])
        return None

def explore_contact_properties():
    """Get all contact properties to understand available fields"""
    print("\n" + "="*60)
    print("CONTACT PROPERTIES")
    print("="*60)

    data = api_get("/crm/v3/properties/contacts")
    if not data:
        return []

    properties = data.get("results", [])

    # Group by source (HubSpot vs custom)
    hubspot_props = []
    custom_props = []

    for prop in properties:
        info = {
            "name": prop.get("name"),
            "label": prop.get("label"),
            "type": prop.get("type"),
            "description": prop.get("description", "")[:100]
        }
        if prop.get("hubspotDefined"):
            hubspot_props.append(info)
        else:
            custom_props.append(info)

    # Show custom properties first (most interesting)
    print(f"\n📌 CUSTOM PROPERTIES ({len(custom_props)} found)")
    print("-"*40)
    for p in sorted(custom_props, key=lambda x: x["name"]):
        print(f"  • {p['name']}: {p['label']} ({p['type']})")
        if p["description"]:
            print(f"    └─ {p['description']}")

    # Show relevant HubSpot properties for attribution
    attribution_props = [p for p in hubspot_props if any(kw in p["name"].lower() for kw in
        ["source", "campaign", "medium", "first", "recent", "original", "conversion", "form", "page"])]

    print(f"\n📊 ATTRIBUTION-RELATED PROPERTIES ({len(attribution_props)} found)")
    print("-"*40)
    for p in sorted(attribution_props, key=lambda x: x["name"]):
        print(f"  • {p['name']}: {p['label']}")

    return properties

def explore_forms():
    """Get all marketing forms"""
    print("\n" + "="*60)
    print("MARKETING FORMS")
    print("="*60)

    data = api_get("/marketing/v3/forms")
    if not data:
        return []

    forms = data.get("results", [])
    print(f"\n📝 Found {len(forms)} forms")
    print("-"*40)

    for form in forms:
        print(f"\n  • {form.get('name')}")
        print(f"    ID: {form.get('id')}")
        print(f"    Type: {form.get('formType')}")
        created = form.get("createdAt", "")[:10]
        print(f"    Created: {created}")

        # Show fields
        fields = form.get("fieldGroups", [])
        field_names = []
        for group in fields:
            for field in group.get("fields", []):
                field_names.append(field.get("name"))
        if field_names:
            print(f"    Fields: {', '.join(field_names[:5])}{'...' if len(field_names) > 5 else ''}")

    return forms

def explore_lists():
    """Get contact lists"""
    print("\n" + "="*60)
    print("CONTACT LISTS")
    print("="*60)

    # Try legacy lists API
    data = api_get("/contacts/v1/lists", params={"count": 100})
    if not data:
        # Try newer API
        data = api_get("/crm/v3/lists")

    if not data:
        print("Could not retrieve lists")
        return []

    lists = data.get("lists", data.get("results", []))
    print(f"\n📋 Found {len(lists)} lists")
    print("-"*40)

    for lst in lists[:20]:  # Show first 20
        name = lst.get("name")
        list_id = lst.get("listId", lst.get("id"))
        count = lst.get("metaData", {}).get("size", lst.get("memberCount", "?"))
        list_type = lst.get("listType", lst.get("processingType", ""))
        print(f"  • {name} ({count} contacts) - {list_type}")
        print(f"    ID: {list_id}")

    if len(lists) > 20:
        print(f"  ... and {len(lists) - 20} more")

    return lists

def explore_sample_contacts():
    """Get sample contacts to see actual data"""
    print("\n" + "="*60)
    print("SAMPLE CONTACTS (Recent 10)")
    print("="*60)

    # Get contacts with key properties
    properties_to_fetch = [
        "email", "firstname", "lastname", "createdate",
        "hs_analytics_source", "hs_analytics_source_data_1", "hs_analytics_source_data_2",
        "hs_analytics_first_url", "hs_analytics_first_referrer",
        "recent_conversion_event_name", "first_conversion_event_name",
        "lifecyclestage", "hs_lead_status"
    ]

    data = api_get("/crm/v3/objects/contacts", params={
        "limit": 10,
        "properties": ",".join(properties_to_fetch),
        "sorts": "-createdate"
    })

    if not data:
        return []

    contacts = data.get("results", [])
    print(f"\n👥 Showing {len(contacts)} most recent contacts")
    print("-"*40)

    for contact in contacts:
        props = contact.get("properties", {})
        email = props.get("email", "no email")
        source = props.get("hs_analytics_source", "unknown")
        source_detail = props.get("hs_analytics_source_data_1", "")
        first_url = props.get("hs_analytics_first_url", "")
        conversion = props.get("first_conversion_event_name", "")
        created = props.get("createdate", "")[:10]

        print(f"\n  📧 {email}")
        print(f"     Source: {source}" + (f" ({source_detail})" if source_detail else ""))
        print(f"     First URL: {first_url[:60]}..." if first_url and len(first_url) > 60 else f"     First URL: {first_url or 'N/A'}")
        print(f"     Conversion: {conversion or 'N/A'}")
        print(f"     Created: {created}")

    return contacts

def explore_source_breakdown():
    """Get breakdown of contacts by source"""
    print("\n" + "="*60)
    print("SOURCE BREAKDOWN (Aggregated)")
    print("="*60)

    # Search for contacts grouped by source
    # We'll do this by querying and counting
    sources = {}

    # Get a larger sample to analyze
    all_contacts = []
    after = None

    for _ in range(5):  # Get up to 500 contacts
        params = {
            "limit": 100,
            "properties": "hs_analytics_source,hs_analytics_source_data_1,first_conversion_event_name,createdate"
        }
        if after:
            params["after"] = after

        data = api_get("/crm/v3/objects/contacts", params=params)
        if not data:
            break

        contacts = data.get("results", [])
        all_contacts.extend(contacts)

        paging = data.get("paging", {})
        after = paging.get("next", {}).get("after")
        if not after:
            break

    print(f"\n📈 Analyzed {len(all_contacts)} contacts")
    print("-"*40)

    # Count by source
    for contact in all_contacts:
        props = contact.get("properties", {})
        source = props.get("hs_analytics_source", "UNKNOWN")
        source_detail = props.get("hs_analytics_source_data_1", "")
        conversion = props.get("first_conversion_event_name", "")

        key = source
        if source_detail:
            key = f"{source} | {source_detail}"

        if key not in sources:
            sources[key] = {"count": 0, "conversions": {}}
        sources[key]["count"] += 1

        if conversion:
            if conversion not in sources[key]["conversions"]:
                sources[key]["conversions"][conversion] = 0
            sources[key]["conversions"][conversion] += 1

    # Display sorted by count
    print("\n📊 BY SOURCE:")
    for source, data in sorted(sources.items(), key=lambda x: -x[1]["count"]):
        print(f"  • {source}: {data['count']} contacts")
        if data["conversions"]:
            for conv, cnt in sorted(data["conversions"].items(), key=lambda x: -x[1])[:3]:
                print(f"    └─ {conv}: {cnt}")

def main():
    print("🔍 HubSpot Data Explorer")
    print(f"   Running at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)

    # Run all explorations
    explore_contact_properties()
    explore_forms()
    explore_lists()
    explore_sample_contacts()
    explore_source_breakdown()

    print("\n" + "="*60)
    print("✅ Exploration complete!")
    print("="*60)

if __name__ == "__main__":
    main()
