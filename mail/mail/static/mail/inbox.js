document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);


    // By default, load the inbox
    load_mailbox('inbox');
  });
  

  function compose_email() {
  
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    document.querySelector('#compose-form').onsubmit = (e) => { 
      //Prevent inbox from being displayed after
        e.preventDefault();
        fetch('/emails', {
          method: 'POST',
          read: false,
          body: JSON.stringify({
              recipients: document.querySelector('#compose-recipients').value,
              subject: document.querySelector('#compose-subject').value,
              body: document.querySelector('#compose-body').value
          })
        })
        .then(response => response.json())
        .then(result => {
          // Print result
          //If an error occurs display a styled error message
            if (result["error"]) {
                document.querySelector('#error').innerHTML = `<div class="alert alert-danger alert-dismissible" role="alert">${result["error"]}</div>` 
                document.querySelector('#error').style.display = 'block';
              }
              else {
                document.querySelector('#message').style.display = 'none';
                load_mailbox('sent')
              }
            document.querySelector('#message').style.display = 'none';   
        });
      }

  }

  
  
  function load_mailbox(mailbox) {

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(email => {
    // Print email
    console.log(email);
      // For each GET request create a card to display its details
    email.forEach(element => {
        const e = document.createElement('div');
        //If read display as gray
        if (element["read"] == true) {
        e.innerHTML = `
        <div id="divs" class="card" style="cursor: pointer; background-color: rgba(226, 226, 226, 0.849);">
        <div class="card-body">
        <ul class="navbar" style="list-style-type: none;">
            <li class="nav-item">
                <h5 class="card-title"><b>${element["sender"]}</b></h5>
            </li>
            <li class="nav-item>
                <h5 class="card-title">${element["subject"]}</h5>
            </li>
            <li class="nav-item>
                <small class="text-muted">${element["timestamp"]}</small>
            </li>
            <li class="nav-item">     
                <span class="navbar-text">
                    <i id="archicon" class="fas fa-archive fa-2x"></i>
                </span> 
            </li>
        </ul>
        </div>
        </div> `
        } else {
        e.innerHTML = `
      
        <div class="card" id="divs" style="cursor: pointer;">
        <div style="position: absolute; bottom: 25px; left: 45px;"> <span class="badge badge-pill badge-secondary">New</span></div>
        <div class="card-body">
        <ul class="navbar" style="list-style-type: none;">
            <li class="nav-item">
                <h5 class="card-title"><b>${element["sender"]}</b></h5>
            </li>
            <li class="nav-item>
                <h5 class="card-title">${element["subject"]}</h5>
            </li>
            <li class="nav-item>
                <small class="text-muted">${element["timestamp"]}</small>
            </li>
            <li class="nav-item">     
                <span class="navbar-text">
                <i class="fas fa-archive fa-2x"></i>
                </span> 
            </li>
        </ul>
        </div>
        </div> `
      };

      document.querySelector('#emails-view').append(e);
      
      //If email is clicked
      e.addEventListener('click', function() {
        document.querySelector('#email-view').style.display = 'block';
        document.querySelector('#emails-view').style.display = 'none';
      
        fetch(`/emails/${element["id"]}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
      //Individual email information
        document.querySelector('#email-view').innerHTML = `
          <h5><br>${element["subject"]}</h5>
          <br>
          <h5><i class="far fa-user-circle fa-2x"></i>               <span style="font-weight: bold;">${element["sender"]}</span><span style="font-size: 12px;" class="text-muted">         ${element["timestamp"]}</span></h5> 

            <span class="text-muted">To: ${element["recipients"]}</span> <br>
          <hr>
          ${element["body"]}
          <hr>
          <div>
            <button class="btn btn-sm btn-outline-dark" id="re">Reply</button>
            <button class="btn btn-sm btn-outline-dark" id="arch">${element["archived"]?"Unarchive":"Archive"}</button>
          </div>
          `
        
      
          
        //If reply button is cicked
        document.querySelector('#re').addEventListener('click', function() {

            compose_email();
          // If the email is not already a reply to a previous email
            if(element["subject"].slice(0,4) != 'Re: '){
              element["subject"] = `Re: ${element['subject']}`;
            }

            document.querySelector('#compose-recipients').value = element['sender']; 
            document.querySelector('#compose-subject').value = `${element['subject']}`;
            document.querySelector('#compose-body').value = `On ${element['timestamp']} ${element['sender']} wrote: \n\n ${element['body']} \n\n_____________________________________________________________________________________________________________`;
          });

          //If archive button is clicked
          document.querySelector('#arch').addEventListener('click', function() {
            if(element["archived"] == false){
            fetch(`/emails/${element["id"]}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: true
                })
              })
              load_mailbox('inbox');
            } else {
                fetch(`/emails/${element["id"]}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        archived: false
                    })
                })
                load_mailbox('inbox');
            }
            
        });
        });
      
      });
    }); 
    // ... do something else with email ...
    
    
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

  
    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3><i class="fas fa-inbox fa-1x"></i>        ${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    };

