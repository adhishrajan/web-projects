/*
This js file is to dynamically create the question and answer labels on the new quiz html page.
*/

var i = 0;

// variable createform is a function that creates an input for a question and 3 answer choices
const createform = () => {
    var br = document.createElement("br");
    const form = document.getElementById("forma");

    var body = document.createElement("input");
    body.setAttribute("type", "text");
    body.setAttribute("name", `body${i}`);
    body.setAttribute("placeholder", "Question");
    var abody1 = document.createElement("input");
    abody1.setAttribute("type", "text");
    abody1.setAttribute("name", `abody1${i}`);
    abody1.setAttribute("placeholder", "Answer");
    var correct1 = document.createElement("input");
    correct1.setAttribute("type", "checkbox");
    correct1.setAttribute("name", `correct1${i}`);
    correct1.setAttribute("value", `correct1${i}`);
    var label1 = document.createElement("label");
    label1.setAttribute("for", `correct1${i}`); 

    var abody2 = document.createElement("input");
    abody2.setAttribute("type", "text");
    abody2.setAttribute("name", `abody2${i}`);
    abody2.setAttribute("placeholder", "Answer");
    var correct2 = document.createElement("input");
    correct2.setAttribute("type", "checkbox");
    correct2.setAttribute("name", `correct2${i}`);
    correct2.setAttribute("value", `correct2${i}`);
    var label2 = document.createElement("label");
    label2.setAttribute("for", `correct2${i}`); 

    var abody3 = document.createElement("input");
    abody3.setAttribute("type", "text");
    abody3.setAttribute("name", `abody3${i}`);
    abody3.setAttribute("placeholder", "Answer");
    var correct3 = document.createElement("input");
    correct3.setAttribute("type", "checkbox");
    correct3.setAttribute("name", `correct3${i}`);
    correct3.setAttribute("value", `correct3${i}`);
    var label3 = document.createElement("label");
    label3.setAttribute("for", `correct3${i}`); 

    body.style.alignItems = "center";
    form.appendChild(body);
    form.appendChild(document.createElement('br'));

    abody1.style.alignItems = "center";
    correct1.style.alignItems = "center";
    label1.style.alignItems = "center";
    form.appendChild(abody1);
    form.appendChild(correct1);
    form.appendChild(label1);
    form.appendChild(document.createElement('br'));
    
    abody2.style.alignItems = "center";
    correct2.style.alignItems = "center";
    label2.style.alignItems = "center";
    form.appendChild(abody2);
    form.appendChild(correct2);
    form.appendChild(label2);  
    form.appendChild(document.createElement('br'));

    abody3.style.alignItems = "center";
    correct3.style.alignItems = "center";
    label3.style.alignItems = "center";
    form.appendChild(abody3);
    form.appendChild(correct3);
    form.appendChild(label3);  
    form.appendChild(document.createElement('br'));

    form.appendChild(document.createElement('br'));
    form.appendChild(document.createElement('br'));
  

    document.getElementsByTagName("body")[0]
    .appendChild(form);

    i++;

}

document.addEventListener('DOMContentLoaded', function() {


    // for each question in "questionamt", run createform
    document.querySelector('#bro').addEventListener('click', () => {
        for (var i = 0; i < document.querySelector('#questionamt').value; i++)
        {
            createform();
        }
        document.getElementById("bro").style.display = "none";
        document.getElementById("sub").style.display = "block";
    })
    
})
