function editpost(id){
    
    fetch(`/postapi/${id}`)
.then(response => response.json())
.then(blogpost => {
    // Print email
    cardbody = document.querySelector(`#card-body-${id}`);
    cardbody.innerHTML = `<form id="editform-${blogpost.id}"><div class="form-group"><label for="textarea">Edit your post:</label>
    <textarea class="form-control" id="textarea-${blogpost.id}" rows="5">${blogpost.content}</textarea><br><button class="btn btn-primary" type="submit">Save</button></form>`;
    // ... do something else with email ...
    const form = document.querySelector(`#editform-${blogpost.id}`);
    form.onsubmit = () => {
        const textarea = document.querySelector(`#textarea-${blogpost.id}`).value;
        fetch(`/postapi/${blogpost.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: textarea,
                username: blogpost.username
            })
          })
        showcontent(`${blogpost.id}`);
        return false;
    }
});
}

function showcontent(id){
    cardbody = document.querySelector(`#card-body-${id}`);
    fetch(`/postapi/${id}`)
.then(response => response.json())
.then(blogpost => {
    // Print email
     cardbody.innerHTML = `<p>${blogpost.content}</p>`;
    // ... do something else with email ...
});
}