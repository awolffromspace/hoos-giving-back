# Hoos Giving Back: Project-1-34

A micro-donations and micro-volunteering web application where users can donate to multiple charities, volunteer to perform requested tasks, and view others' donations and volunteering through a feed. Users level up with each donation of $10 or each volunteered time of 30 minutes.

Link: https://project-1-34.herokuapp.com

## Donations

On the donate page, move the sliders to specify the amount of money to donate for each charity. While the maximum slider value is only $100 to make it accurate enough to select small values, higher values can be submitted in the input boxes. After submitting, the Stripe API will ask for credit card information, which can be filled in with a test credit card by repeatedly typing "42" over and over.

## Volunteering

Just like donations, the volunteer page has sliders to set how many minutes to volunteer for each task. However, each task has a goal amount, which is the total amount of minutes requested by the task submitter. Each time a user volunteers to perform a task, that task's goal will be reduced by however much time the user volunteered for. Once the goal is met, the task will be hidden from view, indicating that the task is complete. Additionally, users can submit new tasks by clicking on "Submit a new task!"

## Screenshots

![front page](https://github.com/awolffromspace/hoos-giving-back/blob/master/screenshots/front_page.png?raw=true)

![donate](https://github.com/awolffromspace/hoos-giving-back/blob/master/screenshots/donate.png?raw=true)

![credit card API](https://github.com/awolffromspace/hoos-giving-back/blob/master/screenshots/credit_card_api.png?raw=true)

![feed](https://github.com/awolffromspace/hoos-giving-back/blob/master/screenshots/feed.png?raw=true)

![volunteer](https://github.com/awolffromspace/hoos-giving-back/blob/master/screenshots/volunteer.png?raw=true)

![task submission](https://github.com/awolffromspace/hoos-giving-back/blob/master/screenshots/task_submission.png?raw=true)
