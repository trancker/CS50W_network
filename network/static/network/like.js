function likepost(id,likedby){
    console.log(`id:${id}\nliked by:${likedby}`)
    fetch(`/postapi/${id}`)
.then(response => response.json())
.then(blogpost => {
    // Print email
    console.log(blogpost);
    const likescount = blogpost.likes


    fetch(`/likesapi/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            "id":id,
            "likedby":likedby[0],
            "likes":likescount+1
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
          likesdiv = document.querySelector(`#likes-${id}`)
          likesdiv.innerHTML = `<p><img class="unlikebtn" id="unlikebtn-${id}" src="https://img.icons8.com/cotton/64/000000/like--v1.png"/> <b>${likescount+1}</b></p>`
          unlikebtn = document.querySelector(`#unlikebtn-${id}`)
          unlikebtn.onclick = ()=> {
            unlikepost(id,likedby)
                                    }
      });

    // ... do something else with email ...
});
    }

function unlikepost(id,unlikedby){
    console.log(`id: ${id}\nunlikedby: ${unlikedby}`)
    fetch(`/postapi/${id}`)
    .then(response => response.json())
    .then(bpost => {
// Print email
                console.log(bpost.likes);
                const likescount = bpost.likes
                fetch(`/likesapi/${id}`, {
                    method: 'DELETE',
                    body: JSON.stringify({
                        "id": id,
                        "unlikedby": unlikedby[0],
                        "likes": likescount-1
                    })
                  })
                  .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
          likesdiv = document.querySelector(`#likes-${id}`)
          likesdiv.innerHTML = `<p><img class="likebtn" id="likebtn-${id}" src="https://img.icons8.com/ios/50/000000/like.png"/> <b>${likescount-1}</b></p>`
          likebtn = document.querySelector(`#likebtn-${id}`)
          likebtn.onclick = ()=> {
            likepost(id,unlikedby)
                                    }
      });
                // ... do something else with email ...
                    });
}

    