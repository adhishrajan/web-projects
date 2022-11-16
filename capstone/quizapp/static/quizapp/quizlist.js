// This js file displays the quiz information on the modal for each quiz when clicked

document.addEventListener('DOMContentLoaded', () => {
    // make an array of all buttons
    const modals = [...document.getElementsByClassName('modal-button')];

    
    const modalsbody = document.getElementById('modbody');

    //start button
    const start = document.getElementById('start');

    // display each button in console when clicked
    modals.forEach(modalBtn => modalBtn.addEventListener('click', () => {
        const pk = modalBtn.getAttribute('data-pk');
        const subject = modalBtn.getAttribute('data-subject');
        const name = modalBtn.getAttribute('data-quiz');
        const questionamt = modalBtn.getAttribute('data-questions');
        const time = modalBtn.getAttribute('data-time');
        const difficulty = modalBtn.getAttribute('data-difficulty');
        const passingscore = modalBtn.getAttribute('data-pass');
        const creator = modalBtn.getAttribute('data-creator');

        modalsbody.innerHTML = `
        
        <div class="h5 mb-3">Start "<b>${name}</b>"? </div>
        <div class="text-muted">
            <ul>
                <li>Creator: <b>${creator}</b></li>
                <li>Subject: <b>${subject}</b></li>
                <li>Difficulty: <b>${difficulty}</b></li>
                <li>Number of Questions: <b>${questionamt}</b></li>
                <li>Score Required to Pass: <b>${passingscore}%</b></li>
                <li>Time Allotted: <b>${time} Minutes</b></li>
            </ul>
        </div>
        `
        // When start quiz button is clicked
        start.addEventListener('click', () => {
            //set window location href to the specific quiz view
            window.location.href = "/" + pk;
        })
    }))

})



