#!/bin/sh

rm -f flask_app/create_node_network/round_data/*.json # remove custom LLM JSON files
rm -f flask_app/llm_api/llm_files/*.* # remove custom LLM files
echo Cleaned up round_data and llm_file directory files