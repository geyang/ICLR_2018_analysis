# Analyzing ICLR 2018 Submission and Review Data

I did some analysis on the submissions to this ICLR (2018). Looks like the average rating is just above 5.

## Distribution of ratings

![all_scores.png](./figures/all_scores.png)
Pink histogram shows the distribution of the average rating for each submission. Blue shows that of all ratings data without being bucketed by submission.

- The ratings are mostly center around 5 (5.23 to be exact). 
- The distribution of scores is skewed and asymmetric
- Virtually no 10, with a few 1's

| Stats      | Result |
|:---------- |:------ |
| mean       | 5.23   |
| median     | 5.33   |
| our rating | 5.33   |


## When Do People Submit, Comment, or Review?

It is also interesting to look at when people submit their paper and reviews. Figure below shows the submission frequency versus time. 

![./figures/submission_timeline.png](./figures/submission_timeline.png)

Looks like people start looking at the papers as soon as the review period starts! The actual reviewers though, only do so half way through. It is unclear if this have something to do with how the review assignments are arranged and handed out.

Also interestingly, people comment much less on Sundays! The comment frequency shows strong weekly cyclicity. On the other hand, the review submissions are not. A possible explanation is that reviewers tend to be grad students and junior professors, who don't have a lot of family commitments.

## Is it better to submit later?

- [ ] todo: look at the distribution w.r.t. submissions submitted at different time.
