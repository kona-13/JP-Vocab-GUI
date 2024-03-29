Tkinter application that pulls vocabulary from vocab.csv.

By default it pulls in order - but this can be changed from the order button.

![image](https://github.com/kona-13/JP-Vocab-GUI/assets/77511759/e20e9e44-2696-4a3d-a787-3e02d7b74e16)


This application is intended to be used to learn and review vocab.

Download the zip and extract contents to folder for executable version.

The words were sourced from this list: https://docs.google.com/spreadsheets/d/13PjfuQSsbkixNGj_9U271M6eqGVVWp5ATRivKlN06S4/edit#gid=0

Feel free to do whatever you want with this. The .csv format is: Kanji, Kana, Meaning, Type (i.e. Noun), JLPT Level*. Laying out another dataset like this and naming it vocab.csv will work fine (e.g. https://imgur.com/a/Q3nAGUk).

*This dataset uses the old JLPT levels - so it predates the N5 - N1, instead using JLPT4 - JLPT1, with an additional set of words under JLPT0 - see: https://en.wikipedia.org/wiki/Japanese-Language_Proficiency_Test#Older_edition

I used this font - so you will probably need it: https://fonts.google.com/noto/specimen/Noto+Sans+JP

A guide on how to add the font (Windows): https://support.microsoft.com/en-us/office/add-a-font-b7c5f17c-4426-4b53-967f-455339c564c1

Issues to resolve:

1.) Tkinter traceback line 105 on random order mode on v1.06 (possibly on other versions) - this happens randomly and can be ignored by hitting reset for now - but I will attempt to figure out what is causing it.

Plan to add:

1.) Optional setting to record wrongs. The ability to use this list of wrongs as a dataset instead of vocab.csv

2.) Radio buttons to exclude vocab by level.

3.) Audio?
