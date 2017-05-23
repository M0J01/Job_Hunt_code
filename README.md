# Job_Search_Hunt
First itteration of Job Hunting Software

00_Ca_Robotics is the current working version. Boston and New York versions are depricated.

Running 00_Ca_Robotics will generate a text file with ranked job results and link to job posting.

Job ranking is currently done by a weighted keyword list. Disqualifying words are currently commented out due to over correction and ranking issues.


Things it would be cool to add::

*Increased Functionality*

-GUI for a user to type in a list of key words, or add past them from a text file. -Turn all HTML to lower case in order to cut down on number of keywords that have to be matched ("Matlab" vs "matlab" vs "MATLAB") -better regex recognition of symbols to reduce redundant keywords (" C " vs "C " vs  "C." vs "C,") because "C" could just be at the start of the word "Cool" "Craft" or "Champ". -ability to read job description from currently unreadable sources including; AJAX pages, Apple crazyness, and other pages with weird interfaces. -"Perfect Match" dictionary capabilities added, where perfect hits are stored in a library, and all future hits are matched to their words/keywords as well"
-Add functionality to allow for the cycling through of "Seed Pages" and "Output Pages" this is a quick fix.


*Core Functionality*

-Better sorting algorythms
  +better Disqualifaction Recognition
  +better Ranking system (Previously simply worded great jobs were given a low rank)


