#!/bin/bash
# Simple quiz tester - run with: bash test-quiz.sh

BASE_URL="http://localhost:3000"

echo "=========================================="
echo "  CURRICULOVE - Homeschool Style Quiz"
echo "=========================================="
echo ""

# Start quiz
RESPONSE=$(curl -s -X POST "$BASE_URL/api/quiz/start" -H "Content-Type: application/json" -d '{}')
SESSION_ID=$(echo "$RESPONSE" | jq -r '.sessionId')
QUESTION=$(echo "$RESPONSE" | jq -r '.question')

echo "Session: $SESSION_ID"
echo ""

# Loop through questions
while true; do
  echo "=========================================="
  echo ""
  echo "$QUESTION"
  echo ""

  # Show options (new format - just strings, not objects)
  echo "$RESPONSE" | jq -r '.options | to_entries | .[] | "  \(.key + 1). \(.value)"'
  echo ""

  # Get user input
  read -p "Your choice: " CHOICE
  CHOICE=$((CHOICE - 1))

  # Build the current question for the request (simpler format now)
  CURRENT_Q=$(echo "$RESPONSE" | jq -c '{question: .question, options: .options}')

  # Submit answer
  RESPONSE=$(curl -s -X POST "$BASE_URL/api/quiz/answer" \
    -H "Content-Type: application/json" \
    -d "{\"sessionId\":\"$SESSION_ID\",\"selectedOptionIndex\":$CHOICE,\"currentQuestion\":$CURRENT_Q}")

  IS_COMPLETE=$(echo "$RESPONSE" | jq -r '.isComplete')

  if [ "$IS_COMPLETE" = "true" ]; then
    echo ""
    echo "=========================================="
    echo "  YOUR RESULT"
    echo "=========================================="
    echo ""
    PRIMARY=$(echo "$RESPONSE" | jq -r '.result.primary.name')
    CONFIDENCE=$(echo "$RESPONSE" | jq -r '.result.confidence')
    DESCRIPTION=$(echo "$RESPONSE" | jq -r '.result.primary.description')
    REASONING=$(echo "$RESPONSE" | jq -r '.result.reasoning')

    echo "You are: $PRIMARY"
    echo "Confidence: $CONFIDENCE%"
    echo ""
    echo "$DESCRIPTION"
    echo ""
    echo "Why: $REASONING"
    echo ""
    echo "Secondary matches:"
    echo "$RESPONSE" | jq -r '.result.secondary[] | "  - \(.name)"'
    break
  fi

  QUESTION=$(echo "$RESPONSE" | jq -r '.question')
  Q_NUM=$(echo "$RESPONSE" | jq -r '.questionNumber')

  echo ""
  echo "[Question $Q_NUM]"
done
