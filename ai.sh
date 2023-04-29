#!/bin/zsh

# Check if the required number of arguments are provided
if [ $# -ne 4 ]; then
    echo "Usage: ai [ada|babbage|chat] edit <file_path> <context>"
    exit 1
fi

# Parse the arguments
model=$1
command=$2
file_path=$3
context=$4

# Check if the specified model is valid
case $model in
    ada)
        model="text-ada-001"
        ;;
    babbage)
        model="text-babbage-001"
        ;;
    chat)
        model="gpt-3.5-turbo"
        ;;
    *)
        echo "Invalid model. Allowed models are: ada, babbage, chat."
        exit 1
        ;;
esac

# Check if the command is valid
case $command in
    edit|fix|comment|complete)
        ;;
    *)
        echo "Invalid command. Allowed commands are: edit, fix, comment, complete."
        exit 1
        ;;
esac

# Read the file content
file_content="$(cat $file_path)"

# Construct the prompt
prompt="$context\n\nHere it is:\n$file_content"

# Properly escape the prompt using jq
escaped_prompt=$(echo "$prompt" | jq -R -s -c '.')

# Echo the constructed prompt
echo "Constructed prompt (with escaping):\n\n$escaped_prompt"

# Make an API call to OpenAI using curl
response=$(curl -s -X POST https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "{\"prompt\": $escaped_prompt, \"max_tokens\": 100, \"n\": 1, \"stop\": null, \"temperature\": 0.5}")

# Echo the raw response
echo "\nRaw response from $model:\n\n$response"

# Extract the AI response
ai_response=$(echo "$response" | awk -F'"text":"' '{gsub(/.*"choices":\[\{"text":"/,""); gsub(/","index".*$/, ""); print}' | sed -e 's/\\"/"/g' -e 's/\\\\/\\/g' -e 's/\\n/\n/g')

# Print the AI response
echo "\nExtracted response:\n$ai_response\n"

# Update the file with the AI response
# echo "$ai_response" > $file_path