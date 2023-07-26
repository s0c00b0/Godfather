# Godfather
A text classification AI used for analyzing players' posts in forum mafia and predicting their alignments.

Work in progress.

## The Plan

3 models currently planned: microread, macroread, and post-generation.

The microread model will make judgements based off a single or a few post(s). This is a notoriously inaccurate way of reading players for the vast majority of cases due to a lack of consideration for context. However, microreading involves the simplest model since the task is essentially text classification.

The macroread model will make predictions for all players in a single thread. This is more accurate than microreads since it takes in the bigger picture. This will also require a more complicated custom architecture.

The post-generation model will not only try to predict the players' alignments but also generate a natural language post based on those reads that attempts to imitate what a human mafia player would post. This will most likely involve text-to-text transformers.