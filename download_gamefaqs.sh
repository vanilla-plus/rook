#!/bin/bash

# Check if both folder name and game URL are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./download_gamefaqs.sh <folder_name> <game_url>"
    exit 1
fi

folder_name="$1"
game_url="$2"

# Create the output folder if it doesn't exist
mkdir -p "$folder_name"

# Download the HTML files with wget and save them in a temporary folder called temp
wget -r -l 1 -p -w 5 --accept-regex "/faqs/" --convert-links --adjust-extension "$game_url/faqs" -P temp

# Find all HTML files in the temp folder
find temp -name "*.html" | while read file; do
    # Skip processing the faqs.html file
    if [ "$(basename "$file")" == "faqs.html" ]; then
        continue
    fi

    # Extract the inner text of the "faqtext" div with pup
    content=$(pup "div.faqtext text{}" < "$file")

    # Replace &#39; with an apostrophe, &lt; with <, &gt; with >, and &#34; with " using sed
    content=$(echo "$content" | sed 's/&#39;/'\''/g; s/&lt;/</g; s/&gt;/>/g; s/&#34;/"/g')

    # Save the content to a .txt file with the same name as the original file in the specified folder
    output_file="$folder_name/$(basename "$file" .html).txt"
    echo "$content" > "$output_file"

    # Remove the original HTML file
    rm "$file"
done

# Remove the temp folder and its contents
rm -r temp