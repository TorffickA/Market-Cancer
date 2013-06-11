Market Cancer
========

Post on a Yahoo! Finance message board in bulk by automating the posting process.

Requirements
========
1. [Python 2.x](http://www.python.org/)
2. [Selenium 2.0.0](http://docs.seleniumhq.org/)
3. [Firefox](http://www.mozilla.org/en-US/firefox/new/)

Usage
========
### Single User Credential Use:

> _marketcancer.py [username] [password] "topicscsv.txt" proxy? posts?_
>
> Example:
>
>     python marketcancer.py username@yahoo.com password1234 GOOG "topics.txt" 1 5
> 
> ####In Other Words
>    Post under username@yahoo.com in the GOOG message board using messages from topics.txt behind a proxy 5 times.
>
###Multiple Users' Credentials Use:

> _marketcancer.py "logincredentialscsv.txt" "topicscsv.txt" proxy? posts?_ 
> 
> Example:
>
>     python marketcancer.py "record.txt" GOOG "topics.txt" 1 5
>
> ####In Other Words
>   Post under username@yahoo.com in the GOOG message board using messages from topics.txt behind a proxy 5 times.
>
>



#Example Run (Metastasis; Cancerous spread)
![Example Cancer Spread](http://i.imgur.com/T7qx12x.jpg)

Contact The Developer
==============
Email: SpockThompsonJr@gmail.com

Website: http://GregThompsonJr.com/