# Hoos Giving Back: Project-1-34

A micro-donations and micro-volunteering web application where users can donate to multiple charities, volunteer to perform requested tasks, and view others' donations and volunteering through a feed. Users level up for each donation of $10 or each volunteered time of 30 minutes.

Link: https://project-1-34.herokuapp.com

## Donations

On the donate page, move the sliders to specify the amount of money to donate for each charity. While the maximum value for the slider is only $100 to improve the accuracy of the slider, higher values can be submitted in the input boxes. After submitting, the Stripe API will ask for credit card information, which can be filled in with a test credit card by repeatedly typing "42" over and over.

## Volunteering

Just like donations, the volunteer page has sliders to set how many minutes to volunteer for each task. However, each task has a goal amount, which is the total amount of minutes requested by the task submitter. Each time a user volunteers to perform a task, that task's goal will be reduced by however much time the user volunteered for. Once the goal is met, the task will be hidden from view, indicating that the task is complete. Additionally, users can submit new tasks by clicking on "Submit a new task!"
