Collection of Functions that takes a text decklist imported from MTG Arena for collecting and displaying deck information

Magic: The Gathering is a game that utilizes decks of 60+ trading cards in a multiplayer strategy game. Each card is a discrete entity and all cards share certain attributes such as color, mana cost, and card type. This collection of attributes made this seem like a good way to develop skills for accessing api's and collecting data.

- Control_magic is the overall control file for running the other scripts
- Scryfallapi takes the txt file and pulls data on each card from the scryfall api. It then stores that data as a .json file so the     relevant card data can be accessed locally
- Handfacts and Deckfacts are both functions that can be accessed to pull data from a sampling of the cards
- Multi is a helper function that parses mutli-color cards in order to make determinations about the required mana base. Multi utilizes the Karsten.json file as the chart for determining mana costs (the multi function is more esoteric to Magic: The Gathering).
- UW_Control_ELD.txt is a sample decklist to work with
