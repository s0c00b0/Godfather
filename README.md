# Godfather

A machine learning model used for analyzing players' posts in forum mafia, predicting their alignments, and generating its own posts to articulate its reads.

Work in progress. Any contributions would be greatly appreciated.

## What is Mafia?

Mafia is an text-based online forum game that relies on logic and deception. The game consists of two teams, the Town and the Mafia. While the Townies initially outnumber the mafia by a large margin, the Mafia have the advantage of knowing each other's identity and being able to secretly communicate with each other. As players post their thoughts in the game thread, Townies must analyze others and weed out the Mafia while the Mafia tries to blend in and overrun the Town.

For more information on Mafia, visit the [MafiaUniverse Wiki](https://www.mafiauniverse.com/wiki/Main_Page) or read a game on the [MafiaUniverse](https://www.mafiauniverse.com/forums/) forums.

## Features

### Data

The data used to train the models is scraped from automated [Mafia Universe](https://www.mafiauniverse.com/forums/) games using the [Selenium](https://www.selenium.dev/) library into a `.txt` file. The `.txt` file is then preprocessed individually by each of the models into an acceptable input format.

### Models

The project features three models: microread, macroread, and post-generation.

The microread model uses a single post in the thread to make a read on the player who posted it. This model is the simplest among the three as the task is essentially a variant of text classification, and utilizes word embeddings from the [spaCy](https://spacy.io/) library combined with a gradient-boosting classifier model. However, most microreads are likely inaccurate, since there is only so much information that can be derived from a single post without context. *__This model is in the process of being implemented.__*

The macroread model reads through the entire thread and generates reads for all the players in the game. This model will use an architecture similar to that used by OpenAI researchers in the paper [Recursively Summarizing Books with Human Feedback](https://arxiv.org/abs/2109.10862). *__This model has not yet been implemented.__*

The post-generation model incorporates the macroread model but has the additional feature of generating its own natural-language posts that can articulate its reads to others similar to a real human player. This model will use the previous macroread model, as well as a text-to-text transformer similar to that from the paper [Attention Is All You Need](https://arxiv.org/abs/1706.03762). *__This model has not yet been implemented.__*