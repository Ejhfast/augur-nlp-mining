### Workflow

Pipeline Overview:

run-reverb -> filterfields -> filter-actions -> skip-gram -> remove-repeated -> count-grams


Example command: 

python filter-actions.py files/watpad.tsv | ruby skip-gram.rb | python remove-repeated.py | python count-grams.py


First we download a big corpus of literature.

Run Reverb

Next we process all the .txt files in the literature with Reverb, which extracts an ordered list of subject-verb-object relationships and some other data. The default Reverb output is in the tsv format.

Filter Fields

We filter out the fields corresponding to the normalized subject-verb-object relationship. After further filtering non-ascii-decodable strings, we have the format:

	he  do  it
	he  ask  her
	...

Filter Actions
We now filter everything that has a person as its subject (we rely on pronouns: he, she, we, they, etc.) and doesn't have a person as its object. We rename matching subjects as "the person". We filter out all relations that aren't in a constructed "approved" token set: a base set of primitives for our analysis. , replacing them with NOPs. We collapse sequences of N NOPs into a single annotated NOP (e.g., "NOP 247" indicates a sequence of 247 NOPs before the next relation in the list). The output has the format:
	the person  enter  the room
	NOP 3
	the person  open  the window
	NOP 0
	the person  close  the window
	NOP 4
	...


Skip Gram

Next we use the previous output to create ngrams, connected by the interleaved NOPs. We throw away ngrams that are too far away from each other in the text (e.g., throw away ngrams connected through NOP N, where N > 10). We then filter out the ngrams that have the same actions repeated in the first and second place. Example: "the person open the door  the person open the door" is now filtered out. The ngrams have the format
	the person open the door  the person open the door
	the person enter the room  the person open the window
	the person open the window  the person close the window
	...

Count Grams

We then compute frequencies of the ngrams, sort them in descending order, and produce the final output with the format:

	the person close his eyes	the person open his eyes	421
	the person close her eyes	the person open her eyes	245
	the person shake her head	the person shake his head	106
	...

---Additional Notes----

Generating approved-tokens.tsv

To generate this filter, we create a list of unique person-action-object tokens (e.g., "the person shake  his head") along with their frequency counts.
 This file has the format:

	the person  enter  the room  1230
	the person  open  the door  1134
	...

Currently, a manual filter is then implemented to keep a smaller list of approved actions. Example: using (e.g., "grep '\thome' 10-person-to-object.tsv | manual-filter.rb - >> approved-tokens.tsv")
