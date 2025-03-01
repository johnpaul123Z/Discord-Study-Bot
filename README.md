# Discord Study Bot
![image](https://github.com/user-attachments/assets/81f1fcce-2542-4c35-ad62-51b094209432)


# Commands 
```sh
$help: Lists available commands and instructions.
$cool: Sends a random, positive message.
$msg <user_id or mention> <message>: Directly sends a DM to the specified user.
$setlecture <2|3|4>: Changes the lecture material used for questions.

```
# Add your own M/L question
add in this format and place in the lecture file. you will need to too update some in the main.py
```sh
  name=[{
    "question": "What is the definition of 'Pseudorandom Number Generator (PRNG)'?",
    "options": {
      "A": "A deterministic algorithm that takes a fixed-length key and produces a pseudorandom bit sequence.",
      "B": "Designed by Ron Rivest in 1987 for RSA Security.",
      "C": "Designed by Daniel Bernstein in 2005 (Salsa20) and 2008 (ChaCha20)."
    },
    "correct": "A",
    "explanation": "The definition of 'Pseudorandom Number Generator (PRNG)' is: A deterministic algorithm that takes a fixed-length key and produces a pseudorandom bit sequence."
  }]
```
**Discord Study Bot** is an interactive Discord bot that posts multiple-choice questions to your `#general` channel. Simply reply with your answer (A, B, or C) and the bot will immediately let you know if you're right or wrong. If you're wrong, it provides the correct answer along with an explanation.

---

## Features

- **Interactive Learning:** Regularly posts study questions.
- **Instant Feedback:** Tells you immediately if your answer is correct.
- **Educational Insights:** Explains the correct answer if you answer incorrectly.
- **Easy Deployment:** Simple to set up and run.

---


## Getting Started

### Prerequisites

```bash
# You will need a Discord Bot API key.
# Obtain one from the Discord Developer Portal:
# https://discord.com/developers/docs/intro

# Clone the repository
git clone https://github.com/johnpaul123Z/Discord-Study-Bot.git

# Change to the project directory
cd Discord-Study-Bot

# Install the required dependencies
pip install -r requirements.txt


```
# Add Bot to your server
```sh
https://discord.com/oauth2/authorize?client_id=1270491309261459598 
```
