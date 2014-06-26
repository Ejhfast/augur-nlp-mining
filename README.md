### Workflow

Pipeline Overview:

run-reverb -> filterfields -> filter-actions -> skip-gram -> remove-repeated -> count-grams


Example command: 

python filter-actions.py files/watpad.tsv | ruby skip-gram.rb | python remove-repeated.py | python count-grams.py


First we download a big corpus of literature.

Run Reverb

Next we process all the .txt files in the literature with Reverb, which extracts an ordered list of subject-verb-object relationships and some other data. The default Reverb output is in the tsv format

Filter Fields

We filter out the fields corresponding to the normalized subject-verb-object relationship. After further filtering non-ascii-decodable strings, we have the format:

	he  do  it
	he  ask  her
	...

Filter Actions
After we We keep everything that has a person as its subject (we rely on pronouns: he, she, we, they, etc.) and doesn't have a person as its object. We rename matching subjects as "the person". Then we throw away everything that occurs less than N times to produce (N-person-to-object.tsv). This guides our analysis towards concrete actions (e.g., "he enters the room") and strips out a lot of inter-personal junk (e.g., "he said to the person"). 
 Next we create a list of person-action-object tokens (e.g., "the person shake  his head") along with their frequency counts.
 This file has the format:

	the person  enter  the room  1230
	the person  open  the door  1134
	...

Next we construct an "approved" token set: a base set of primitives for our analysis. We can either choose a sufficiently large N on person-action-object tokens (e.g., use 30-person-to-object.tsv) or choose a smaller N and crowdsource (right now, Ethan-source) a smaller list through searching and filtering (e.g., "grep '\thome' 10-person-to-object.tsv | manual-filter.rb - >> approved-tokens.tsv").

Call the approved token list approved-tokens.tsv.

Next we walk through corpus-clean.tsv, convert subject pronouns (again to "the person" or "the people"), and filter out all relations that aren't in appoved-tokens.tsv, replacing them with NOPs. We are smart about this and collapse sequences of N NOPs into a single annotated NOP (e.g., "NOP 247" indicates a sequence of 247 NOPs before the next relation in the list). Call this file corpus-filter-nop.tsv, which has the format:

	the person  enter  the room
	NOP 3
	the person  open  the window
	NOP 0
	the person  close  the window
	NOP 4
	...

Next we break apart corpus-filter-nop.tsv into bigrams, connected by the interleaved NOPs. We throw away bigrams that are too far away from each other in the text (e.g., throw away bigrams connected through NOP N, where N > 10). We write these bigrams (actually, skip-grams) to a new file, corpus-bigrams.tsv, which has the format:

	the person enter the room  the person open the window
	the person open the window  the person close the window
	...

Next we collapse the bigrams to compute frequencies, ordering the set by the bigrams most likely to appear. This is the final output of our process, corpus-bigram-counts.tsv, which has the format:

	the person close his eyes	the person open his eyes	421
	the person close her eyes	the person open her eyes	245
	the person shake her head	the person shake his head	106
	...
