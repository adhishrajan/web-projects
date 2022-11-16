document.addEventListener('DOMContentLoaded', () => {

    const edits = document.querySelectorAll('.hi');

    const edits1 = document.querySelectorAll('.hi2');

    const liis = document.querySelectorAll('.lii');


    liis.forEach(element => {
        element.style.display = 'block';
        element.style.animationPlayState = "paused";
    })

    edits.forEach(element => {
        element.style.display = 'none';
    })

    edits1.forEach(element => {
        element.style.display = 'none';
    })

    


})

    

function edit(id) {



    const edtext = document.querySelector(`#edtext${id}`);
    const postbody = document.querySelector(`#postbody${id}`);
    const edsub = document.querySelector(`#edsub${id}`);
    edtext.value = postbody.value;

    postbody.style.animationPlayState = "running";

    edsub.addEventListener('click', () => {


        fetch('/edit/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                body: edtext.value
            })
        });
        
        edtext.style.display = 'none';
        edsub.style.display = 'none';
        postbody.style.display = "block";  

        document.querySelector(`#postbody${id}`).innerHTML = edtext.value;
    });

    if (edtext.style.display == 'block' && edsub.style.display == 'block') {

        edtext.style.display = "none";
        edsub.style.display = "none";  
        postbody.style.display = "block";  


    } else {

        edtext.style.display = 'block';
        edsub.style.display = 'block';
        postbody.style.display = "none";  


        edtext.value = "";     

    }

    postbody.style.animationPlayState = "paused";

}

function like(id) {
    
    const likesub = document.querySelector(`#likesub${id}`);
    const likenum = document.querySelector(`#likenum${id}`);

    likesub.addEventListener('click', () => {

        if (likesub.firstElementChild.style.color == 'black') {
            fetch('/like/' + id, {
                method: 'PUT',
                body: JSON.stringify({
                    like: true
                })
              })

            likesub.firstElementChild.style.color = 'red';
              
            fetch('/like/'+ id)
            .then(response => response.json())
            .then(post => {
                likenum.innerHTML = post.likes;
            });
        }
        
        else {
            fetch('/like/' + id, {
                method: 'PUT',
                body: JSON.stringify({
                    like: false
                })
              });
              
            likesub.firstElementChild.style.color = 'black';

            fetch('/like/'+`${id}`)
            .then(response => response.json())
            .then(post => {
                likenum.innerHTML = post.likes;
            });
        }
        return false;
    });

}
