import re
import json

__all__ = ["Simplimental"]

class Simplimental:
	def __init__(self, text="This is not a bad idea"):
		self.text = text
		with open('simplimental/afinn.json') as data_file:    
		    self.dictionary = json.load(data_file)

		no_punctunation = re.sub(r"[^a-zA-Z ]+", " ", self.text)
		self.tokens = no_punctunation.lower().split(" ")

		for t in self.tokens:
			if len(t) < 3 and t not in ["no"]:
				self.tokens.remove(t)

	def negativity(self):
		hits = 0
		words = []

		for i in range(len(self.tokens)):
			word = self.tokens[i]
			score = self.dictionary.get(word, 0)

			if i > 0 and self.tokens[i-1] in ["no", "not"]:
				word = "not_" + word
				score = -score if score > 0 else 0

			if score < 0:
				hits -= score
				words.append(word)

		return {
			"score": hits,
			"comparative": float(hits) / len(self.tokens),
			"words": words
		}

	def positivity(self):
		hits = 0
		words = []

		for i in range(len(self.tokens)):
			word = self.tokens[i]
			score = self.dictionary.get(word, 0)

			if i > 0 and self.tokens[i-1] in ["no", "not"]:
				word = "not_" + word
				score = -score if score < 0 else 0

			if score > 0:
				hits += score
				words.append(word)

		return {
			"score": hits,
			"comparative": float(hits) / len(self.tokens),
			"words": words
		}

	def analyze(self):
		negativity = self.negativity()
		positivity = self.positivity()

		return {
			"score": positivity["score"] - negativity["score"],
			"comparative": positivity["comparative"] - negativity["comparative"],
		}
