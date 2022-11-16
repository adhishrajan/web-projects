/* This js file is for the quiz view. 
The timer functionality is coded here as well as the 
ajax requests to get the quiz questions
and display/save the results.
*/

// variable for the href of the window
const url = window.location.href;


//  variables referenced later to display the time, score, and results
document.addEventListener('DOMContentLoaded', () => {
    const score = document.getElementById('score');
    const ydiv = document.getElementById('ydiv');
    const timee = document.getElementById('timee');
})


// timer variable is a function (taking time as input) that makes the timer work
const timer = function(time) {
    
    // if time in minutes is less than 10 (single digit)
    if (time.toString().length < 2) 
    {
        // display time with 0 in front
        timee.innerHTML = `<b>0${time}:00</b>`
    }
    else
    {
        // display time normally
        timee.innerHTML = `<b>${time}:00</b>`
    }

    // subtract time by 1 because minute will go down by one as soon as time starts
    let time1 = time - 1;
    // seconds variable
    let time2 = 60;
    let time2_;
    let time1_;

    // set interval function to change time every 1000 ms
    const interval = setInterval(function() {
        time2 = time2 - 1;
        if (time2 < 0)
        {
            time2 = 59;
            time1 = time1 - 1;
        }
        
        if (time1.toString().length < 2)
        {
            time1_ = '0' + time1;
        }
        else
        {
            time1_ = time1;
        }

        if (time2.toString().length < 2)
        {
            time2_ = '0' + time2;
        }
        else
        {
            time2_ = time2;
        }

        if (time1 === 0 && time2 === 0)
        {
            clearInterval(interval);
            alert('Time over!');
            deliver();
            
        }

        timee.innerHTML = `<b>${time1_}:${time2_}</b>`;

    }, 1000);

}



// ajax request to get the quiz data
$.ajax({
    type: 'GET',
    url: `${url}/quiz_viewcont`,
    // on success run function
    success: function(response){
        const data = response.data
        // for each piece of data
        data.forEach(element => {
            // for loop using question as key and answer as value of all entires (taking element as input)
            for (const [question, answers] of Object.entries(element)){
                // add each question to div "hi"
                const h = document.getElementById('hi');
                h.innerHTML += `
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                    <hr>
        
                `

                // add all answers to each question
                answers.forEach(answer => {
                    h.innerHTML += `
                        <div>
                            <input class="answer" name="${question}" id="${question}_${answer}" type="radio" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `
                })
            }
        });

        // get time
        timer(response.time);

    },
    // log error if request didn't work
    error: function(error){
        console.log(error)
    }
})

// create variable to grab the csrf middlewaretoken
const csrf = document.getElementsByName('csrfmiddlewaretoken');


// function to send the data of the answered quiz via ajax request
const deliver = () => {
    // array of all answers
    const anss = [...document.getElementsByClassName('answer')];
    // empty dictionary
    const data = {}
    // put csrf middleware token from form into dictionary
    data['csrfmiddlewaretoken'] = csrf[0].value,
    anss.forEach(element => {
        // add question as value and answer as key in dictionary
        if (element.checked) 
        {
            data[element.name] = element.value
        }
        else
        {
            // if the question has not been answered
            if (!data[element.name]) 
            {
                data[element.name] = null;
            }
        }
    })
    // AJAX request to submit quiz
    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        // assign data to the dictionary

        data: data,
        success: function(response) {
            console.log(response);
            console.log(response.results);
            // make the form not visibile
            qform.style.display = 'None';

            // display score, rounding decimal to 2 points
            score.innerHTML = `<h1 style="color: black; font-family: "Times New Roman", Times, serif;"> ${response.passed ? 'Congratulations, You Passed!': 'Sorry, You Did Not Pass... '} Your Score: ${response.score.toFixed(2)}% </h1> <br><br>`

            
            // for each result
            response.results.forEach(x => {
                // create div element that will be used to display each answer result
                const y = document.createElement('div');
                // question as key, z as value for each entry of x
                for (const [question, z] of Object.entries(x)) {

                    // add the question to each div
                    y.innerHTML = y.innerHTML + 'Question: ' + question + `<br><br>`;
        
                    // array of boostrap classes and add to div
                    const bootstrap = ['container', 'p-3', 'text-light', 'h3'];
                    y.classList.add(...bootstrap);
                    y.style.borderRadius = "15px";

                    // if the question was not answered, display such 
                    if (z == 'not answered')
                    {
                        y.innerHTML += '- Not Answered';
                        y.classList.add('bg-secondary');
                    }
                    // else if answeered
                    else
                    {
                        const a = z['answered'];
                        const c = z['correct answer'];

                        if (a == c)
                        {
                            y.classList.add('bg-success');
                            y.innerHTML += ` You Answered: ${a}`;

                        }
                        else
                        {
                            y.classList.add('bg-danger');
                            y.innerHTML += ` Correct Answer: ${c}`;
                            y.innerHTML += ` You Selected: ${a}`;
                        }
                    }
                }

                
                // append the new divs to y
                ydiv.append(y);

            })
        },
        error: function(error) {
            console.log(error);
        }
    })

}

// when form submits, run the deliver function
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#qform').addEventListener('submit', function(event) {
        event.preventDefault();

        deliver();
    })
})

 
