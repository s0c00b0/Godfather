# Godfather

## Usage

*__This will be updated as features are implemented.__*

### Fetch Data

Navigate to the `fetch-data` directory and use the username and password from your [Mafia Universe](https://www.mafiauniverse.com/forums/) account as arguments to run `fetch-mu.py` as follows.

```bash
python fetch-mu.py -username [your_username] -password [your_password] 
```

This command gathers all posts from automated games on the front page into a text file `data.txt`. By default, it is saved in the same directory `fetch-data`. You can optionally use `-save_path [directory]` to save `data.txt` in a different directory.

_Note: A [Mafia Universe](https://www.mafiauniverse.com/forums/) account is required to fetch data. If you do not have an account, you can register one for free._

### Microread Model

Navigate to the `microread-model` directory. To train your own model, follow the instructions below. If you wish to use the pre-trained model in `microread-model.pkl`, skip to the prediction step.

First, preprocess the posts you wish to use to train the model using the following command.

```bash
python preprocess.py -load_path [data_path]
```

This command gathers the posts and the alignments of their respective authors from the text file specified by the option `-load_path` into a new file `data.csv`. By default, it is saved in the same directory `microread-model`. You can optionally use `-save_path [directory]` to save `data.csv` in a different directory.

_Note: The file provided by `-load_path` must be a series of quoted BBCode posts separated by lines of `--END_QUOTE_SEPARATOR--`. The output of `fetch_mu.py` is automatically formatted in this manner, but any custom data will need to be formatted to fit these requirements.._

