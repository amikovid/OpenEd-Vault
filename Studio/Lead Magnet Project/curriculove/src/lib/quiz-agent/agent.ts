/**
 * Curriculove Quiz Agent - True Agentic Implementation
 *
 * Uses Claude's tool-use capability to reason about answers
 * and decide what to ask next.
 */

import Anthropic from "@anthropic-ai/sdk";
import { QUIZ_SYSTEM_PROMPT, OPENER_QUESTION } from "./prompt";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// The tools the agent can use
const AGENT_TOOLS: Anthropic.Tool[] = [
  {
    name: "ask_question",
    description: "Ask the user a multiple choice question. Use short, punchy options (5-8 words max).",
    input_schema: {
      type: "object" as const,
      properties: {
        question: {
          type: "string",
          description: "The question to ask (keep it short and direct)",
        },
        options: {
          type: "array",
          items: { type: "string" },
          description: "4-5 short answer options",
        },
        reasoning: {
          type: "string",
          description: "Internal reasoning - why you're asking this, what you're trying to distinguish",
        },
      },
      required: ["question", "options", "reasoning"],
    },
  },
  {
    name: "complete_quiz",
    description: "End the quiz and declare the result. Use when 80%+ confident in primary philosophy.",
    input_schema: {
      type: "object" as const,
      properties: {
        primary: {
          type: "string",
          description: "Primary philosophy tag (CL, CM, MO, WA, TR, UN, WF, PB, MS, NB, EC, FB)",
        },
        confidence: {
          type: "number",
          description: "Confidence percentage (0-100)",
        },
        secondary: {
          type: "array",
          items: { type: "string" },
          description: "Secondary philosophy matches (1-2 tags)",
        },
        reasoning: {
          type: "string",
          description: "Summary of what their answers revealed about their philosophy",
        },
      },
      required: ["primary", "confidence", "secondary", "reasoning"],
    },
  },
];

export interface QuizState {
  history: { question: string; options: string[]; answer: string }[];
  questionCount: number;
}

export interface QuizQuestion {
  question: string;
  options: string[];
  reasoning: string;
}

export interface QuizResult {
  primary: string;
  confidence: number;
  secondary: string[];
  reasoning: string;
}

export type AgentResponse =
  | { type: "question"; data: QuizQuestion }
  | { type: "result"; data: QuizResult };

/**
 * Build the conversation history for the agent
 */
function buildMessages(state: QuizState): Anthropic.MessageParam[] {
  const messages: Anthropic.MessageParam[] = [];

  // Add history as alternating user/assistant messages
  for (const entry of state.history) {
    // Assistant asked the question
    messages.push({
      role: "assistant",
      content: `I'll ask: "${entry.question}"\nOptions: ${entry.options.map((o, i) => `${i + 1}. ${o}`).join(", ")}`,
    });
    // User answered
    messages.push({
      role: "user",
      content: `They chose: "${entry.answer}"`,
    });
  }

  // Prompt for next action
  if (state.history.length === 0) {
    messages.push({
      role: "user",
      content: "Start the quiz. Ask the opening question.",
    });
  } else {
    messages.push({
      role: "user",
      content: `Based on their ${state.questionCount} answers so far, either ask another question to narrow down their philosophy, or if you're confident (80%+), complete the quiz with a result.`,
    });
  }

  return messages;
}

/**
 * Run the agent to get the next question or final result
 */
export async function runQuizAgent(state: QuizState): Promise<AgentResponse> {
  const messages = buildMessages(state);

  // Special case: first question is always the opener
  if (state.history.length === 0) {
    return {
      type: "question",
      data: {
        question: OPENER_QUESTION.question,
        options: OPENER_QUESTION.options,
        reasoning: "Starting with the standard opener to broadly bucket their motivation",
      },
    };
  }

  const response = await anthropic.messages.create({
    model: "claude-3-5-haiku-20241022",
    max_tokens: 1024,
    system: QUIZ_SYSTEM_PROMPT,
    tools: AGENT_TOOLS,
    messages,
  });

  // Find the tool use in the response
  const toolUse = response.content.find(
    (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
  );

  if (!toolUse) {
    // Fallback: if no tool use, try to parse from text
    const textBlock = response.content.find(
      (block): block is Anthropic.TextBlock => block.type === "text"
    );

    if (textBlock) {
      try {
        const parsed = JSON.parse(textBlock.text);
        if (parsed.type === "question") {
          return { type: "question", data: parsed };
        } else if (parsed.type === "result") {
          return { type: "result", data: parsed };
        }
      } catch {
        // Couldn't parse
      }
    }

    throw new Error("Agent did not use a tool or return valid JSON");
  }

  if (toolUse.name === "ask_question") {
    const input = toolUse.input as {
      question: string;
      options: string[];
      reasoning: string;
    };
    return {
      type: "question",
      data: {
        question: input.question,
        options: input.options,
        reasoning: input.reasoning,
      },
    };
  }

  if (toolUse.name === "complete_quiz") {
    const input = toolUse.input as {
      primary: string;
      confidence: number;
      secondary: string[];
      reasoning: string;
    };
    return {
      type: "result",
      data: {
        primary: input.primary,
        confidence: input.confidence,
        secondary: input.secondary,
        reasoning: input.reasoning,
      },
    };
  }

  throw new Error(`Unknown tool: ${toolUse.name}`);
}
