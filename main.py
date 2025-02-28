
import discord
import os
import re
import random
from datetime import datetime

my_secret = os.environ['apikey']
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Global variable to store the current active question
active_question = None

# List of multiple-choice questions covering all provided topics.
# Each question is a dictionary with keys: "question", "options", "correct", "explanation"
question_list = [
    {
        "question": "Which security principle restricts information access exclusively to authorized parties?",
        "options": {
            "A": "Confidentiality",
            "B": "Integrity",
            "C": "Availability"
        },
        "correct": "A",
        "explanation": "Confidentiality ensures that information is accessible only to authorized parties."
    },
    {
        "question": "Which security principle ensures that data remains accurate and unaltered?",
        "options": {
            "A": "Confidentiality",
            "B": "Integrity",
            "C": "Availability"
        },
        "correct": "B",
        "explanation": "Integrity ensures that data is accurate and unmodified."
    },
    {
        "question": "Which security principle guarantees that authorized users can access information when needed?",
        "options": {
            "A": "Integrity",
            "B": "Confidentiality",
            "C": "Availability"
        },
        "correct": "C",
        "explanation": "Availability ensures that information is accessible to authorized users when needed."
    },
    {
        "question": "What term describes the situation when data integrity is compromised due to tampering?",
        "options": {
            "A": "Integrity Violation",
            "B": "Confidentiality Breach",
            "C": "Availability Failure"
        },
        "correct": "A",
        "explanation": "Integrity Violation occurs when data has been tampered with."
    },
    {
        "question": "Which methods are typically implemented to achieve confidentiality in data handling?",
        "options": {
            "A": "Encryption, Access Controls, and Secure Protocols",
            "B": "Redundant Systems and Failover Mechanisms",
            "C": "Data Backups and Recovery Plans"
        },
        "correct": "A",
        "explanation": "Encryption, access controls, and secure protocols (like HTTPS) help achieve confidentiality."
    },
    {
        "question": "What is the primary purpose of hashing in data security?",
        "options": {
            "A": "Encrypting data for confidentiality",
            "B": "Converting data to a fixed-length value to verify integrity",
            "C": "Providing redundant systems for availability"
        },
        "correct": "B",
        "explanation": "Hashing converts data into a fixed-length hash value to detect any alteration."
    },
    {
        "question": "Why is system availability critical in cybersecurity?",
        "options": {
            "A": "It prevents unauthorized access.",
            "B": "It ensures that users can access necessary information.",
            "C": "It verifies the accuracy of data."
        },
        "correct": "B",
        "explanation": "Availability ensures that authorized users can access necessary information when needed."
    },
    {
        "question": "What is the purpose of developing an attacker model in cybersecurity?",
        "options": {
            "A": "To define an attacker's capabilities and design effective defenses.",
            "B": "To encrypt data during transmission.",
            "C": "To backup and restore system data."
        },
        "correct": "A",
        "explanation": "An attacker model defines an attacker's capabilities, knowledge, and objectives to better plan defenses."
    },
    {
        "question": "Which type of attacker eavesdrops on communications without modifying them?",
        "options": {
            "A": "Active Attacker",
            "B": "Passive Attacker",
            "C": "Insider Threat"
        },
        "correct": "B",
        "explanation": "A passive attacker eavesdrops without altering the communication."
    },
    {
        "question": "Which type of attacker actively modifies or injects malicious data into communications?",
        "options": {
            "A": "Active Attacker",
            "B": "Passive Attacker",
            "C": "Cybercriminal"
        },
        "correct": "A",
        "explanation": "An active attacker alters, interrupts, or injects malicious data into communications."
    },
    {
        "question": "What term describes a security approach that relies solely on hiding system details?",
        "options": {
            "A": "Security by Obscurity",
            "B": "Transparent Security",
            "C": "Multi-Factor Authentication"
        },
        "correct": "A",
        "explanation": "Security by obscurity relies on secrecy of design rather than robust security measures."
    },
    {
        "question": "How does transparency in security contribute to overall system protection?",
        "options": {
            "A": "It prevents all cyber attacks.",
            "B": "It allows independent review to identify vulnerabilities.",
            "C": "It encrypts all data."
        },
        "correct": "B",
        "explanation": "Transparency allows independent researchers to identify and help fix vulnerabilities."
    },
    {
        "question": "What is a primary motivation for cybercriminals?",
        "options": {
            "A": "Political control",
            "B": "Financial gain",
            "C": "System integrity"
        },
        "correct": "B",
        "explanation": "Cybercriminals are typically motivated by financial gain."
    },
    {
        "question": "What is the main objective of cyberwarfare?",
        "options": {
            "A": "Causing disruption or gathering intelligence for political or military purposes.",
            "B": "Encrypting data for secure communications.",
            "C": "Maintaining system availability."
        },
        "correct": "A",
        "explanation": "Cyberwarfare is aimed at causing disruption or gathering intelligence for political/military goals."
    },
    {
        "question": "Which field focuses on securing communications using techniques such as encryption?",
        "options": {
            "A": "Cryptography",
            "B": "Cryptanalysis",
            "C": "Data Backup"
        },
        "correct": "A",
        "explanation": "Cryptography is the science of securing communication through encryption."
    },
    {
        "question": "What is the main focus of cryptanalysis?",
        "options": {
            "A": "Creating encryption algorithms.",
            "B": "Breaking or bypassing encryption.",
            "C": "Setting up secure networks."
        },
        "correct": "B",
        "explanation": "Cryptanalysis is the study of breaking or bypassing encryption."
    },
    {
        "question": "What characterizes symmetric encryption?",
        "options": {
            "A": "It uses the same key for both encryption and decryption.",
            "B": "It uses two different keys.",
            "C": "It requires no key."
        },
        "correct": "A",
        "explanation": "Symmetric encryption uses one key for both processes."
    },
    {
        "question": "What distinguishes asymmetric encryption from symmetric encryption?",
        "options": {
            "A": "It uses no keys.",
            "B": "It uses a single key for both processes.",
            "C": "It uses a pair of keys (public and private)."
        },
        "correct": "C",
        "explanation": "Asymmetric encryption uses two keys: one public and one private."
    },
    {
        "question": "In the encryption equation p = D(E(p, KE), KD), what does the variable 'p' represent?",
        "options": {
            "A": "Plaintext",
            "B": "Ciphertext",
            "C": "Encryption key"
        },
        "correct": "A",
        "explanation": "'p' represents the plaintext (the original message)."
    },
    {
        "question": "In the encryption equation p = D(E(p, KE), KD), what role does 'E' serve?",
        "options": {
            "A": "Encryption function",
            "B": "Decryption function",
            "C": "Encryption key"
        },
        "correct": "A",
        "explanation": "'E' is the encryption function."
    },
    {
        "question": "In the encryption equation p = D(E(p, KE), KD), what does 'KE' denote?",
        "options": {
            "A": "Decryption key",
            "B": "Encryption key",
            "C": "Plaintext"
        },
        "correct": "B",
        "explanation": "'KE' stands for the encryption key."
    },
    {
        "question": "What is the function of 'D' in the encryption equation p = D(E(p, KE), KD)?",
        "options": {
            "A": "Encryption function",
            "B": "Decryption function",
            "C": "Hashing function"
        },
        "correct": "B",
        "explanation": "'D' represents the decryption function."
    },
    {
        "question": "In the encryption equation p = D(E(p, KE), KD), what does 'KD' represent?",
        "options": {
            "A": "Decryption key",
            "B": "Encryption key",
            "C": "Ciphertext"
        },
        "correct": "A",
        "explanation": "'KD' stands for the decryption key."
    },
    {
        "question": "What defines a keyless cipher?",
        "options": {
            "A": "It uses a fixed substitution rule without a key.",
            "B": "It uses a key for encryption and decryption.",
            "C": "It uses asymmetric keys."
        },
        "correct": "A",
        "explanation": "A keyless cipher relies on a fixed substitution rule without the use of a key."
    },
    {
        "question": "What distinguishes a key-based cipher from a keyless cipher?",
        "options": {
            "A": "It does not require any key.",
            "B": "It requires a key for both encryption and decryption.",
            "C": "It uses multiple keys for encryption."
        },
        "correct": "B",
        "explanation": "A key-based cipher requires a key for both encryption and decryption."
    },
    {
        "question": "How does the Caesar Cipher primarily operate?",
        "options": {
            "A": "By shifting letters by a fixed number.",
            "B": "By randomly substituting letters.",
            "C": "By using a complex algorithm."
        },
        "correct": "A",
        "explanation": "The Caesar Cipher encrypts by shifting each letter by a fixed number of positions."
    },
    {
        "question": "In an Affine Cipher, what condition must the variable 'a' satisfy?",
        "options": {
            "A": "It must be a prime number.",
            "B": "It must be coprime with 26.",
            "C": "It must be an even number."
        },
        "correct": "B",
        "explanation": "For decryption in an Affine Cipher, 'a' must be coprime with 26."
    },
    {
        "question": "What is a key feature of the Playfair Cipher that enhances its security?",
        "options": {
            "A": "It encrypts single letters.",
            "B": "It encrypts pairs of letters (digraphs).",
            "C": "It uses no key."
        },
        "correct": "B",
        "explanation": "The Playfair Cipher encrypts pairs of letters, making frequency analysis more difficult."
    },
    {
        "question": "How does the Vigenère Cipher encrypt plaintext?",
        "options": {
            "A": "Using a fixed shift for all letters.",
            "B": "Using a keyword to determine variable shifts.",
            "C": "By reversing the text."
        },
        "correct": "B",
        "explanation": "The Vigenère Cipher uses a keyword to apply different shifts to each letter."
    },
    {
        "question": "What characterizes a known plaintext attack?",
        "options": {
            "A": "The attacker has only ciphertext.",
            "B": "The attacker has both plaintext and corresponding ciphertext.",
            "C": "The attacker has the decryption key."
        },
        "correct": "B",
        "explanation": "In a known plaintext attack, the attacker has access to both the plaintext and its ciphertext."
    },
    {
        "question": "What defines a ciphertext-only attack?",
        "options": {
            "A": "The attacker only has access to ciphertext.",
            "B": "The attacker has both plaintext and ciphertext.",
            "C": "The attacker has the encryption key."
        },
        "correct": "A",
        "explanation": "A ciphertext-only attack is when the attacker has only the ciphertext to work with."
    },
    {
        "question": "How do digital signatures enhance security?",
        "options": {
            "A": "They encrypt data during transmission.",
            "B": "They provide non-repudiation by verifying the origin and authenticity of a message.",
            "C": "They ensure data remains unaltered during storage."
        },
        "correct": "B",
        "explanation": "Digital signatures help verify the message’s origin and authenticity, providing non-repudiation."
    }
]

async def send_new_question(channel):
    """Selects a random question, sets it as active, and sends it as an embed to the channel."""
    global active_question
    active_question = random.choice(question_list)
    embed = discord.Embed(
        title="Multiple Choice Question",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Question", value=active_question["question"], inline=False)
    embed.add_field(name="A", value=active_question["options"]["A"], inline=False)
    embed.add_field(name="B", value=active_question["options"]["B"], inline=False)
    embed.add_field(name="C", value=active_question["options"]["C"], inline=False)
    await channel.send(embed=embed)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Post the first question when the bot starts up
    channel = discord.utils.get(client.get_all_channels(), name="general")
    if channel:
        await send_new_question(channel)
    else:
        print("General channel not found.")

@client.event
async def on_message(message):
    global active_question
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Command handlers (unchanged)
    if message.content.startswith('$help'):
        help_embed = discord.Embed(
            title="Bot Commands Help",
            description=(
                "**$msg <user_id or mention> <message>** - Sends a DM to the specified user.\n"
                "**$cool** - Receive a cool, positive message from the bot."
            ),
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        await message.channel.send(embed=help_embed)
        return

    if message.content.startswith('$cool'):
        cool_messages = [
            "Stay frosty, my friend!",
            "Keep calm and code on.",
            "May your code be bug-free!",
            "Coding is the new magic!"
        ]
        random_message = random.choice(cool_messages)
        cool_embed = discord.Embed(
            title="Cool Vibes",
            description=random_message,
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )
        await message.channel.send(embed=cool_embed)
        return

    if message.content.startswith('$msg'):
        parts = message.content.split(maxsplit=2)
        if len(parts) < 3:
            await message.channel.send("Usage: $msg <user_id or mention> <message>")
            return

        user_identifier = parts[1]
        msg_content = parts[2]

        # Try to extract a user ID from a mention (e.g., <@123456789012345678>)
        user_id = None
        mention_regex = r'<@!?(\d+)>'
        match = re.match(mention_regex, user_identifier)
        if match:
            user_id = int(match.group(1))
        else:
            try:
                user_id = int(user_identifier)
            except ValueError:
                await message.channel.send("Invalid user identifier. Please use a valid user ID or mention.")
                return

        try:
            target_user = await client.fetch_user(user_id)
        except discord.NotFound:
            await message.channel.send("User not found!")
            return
        except discord.HTTPException:
            await message.channel.send("An error occurred while fetching the user.")
            return

        try:
            dm_embed = discord.Embed(
                title="You've Got a Message!",
                description=msg_content,
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            await target_user.send(embed=dm_embed)
            confirm_embed = discord.Embed(
                title="Message Sent!",
                description=f"Your message was sent to {target_user.name}.",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            await message.channel.send(embed=confirm_embed)
        except discord.Forbidden:
            await message.channel.send("I don't have permission to send DMs to that user.")
        return

    # Answer checking in the "general" channel: if the message is "A", "B", or "C" (case-insensitive)
    if message.channel.name == "general" and message.content.strip().lower() in ["a", "b", "c"]:
        # Only process if there is an active question
        if active_question is None:
            return

        user_answer = message.content.strip().upper()
        if user_answer == active_question["correct"]:
            await message.channel.send(f"Good job {message.author.mention}, you're right!")
        else:
            correct_letter = active_question["correct"]
            correct_option = active_question["options"][correct_letter]
            await message.channel.send(
                f"Close but you're wrong, {message.author.mention}. The correct answer is {correct_letter}: {correct_option}.\n{active_question['explanation']}"
            )
        # Reset the active question and send a new one immediately
        active_question = None
        await send_new_question(message.channel)

client.run(my_secret)
