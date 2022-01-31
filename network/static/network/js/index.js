console.log('it is working')

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
console.log(csrftoken)

function handelLikeBtn(e,id){
    fetch('/like',{
        method:'PUT',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body:JSON.stringify({
            id:id
        })
    }).then(res => res.json()).then(res => {
        console.log(res);
        let color = res.color
        e.target.classList = 'btn btn-' +color
        e.target.innerHTML = color == 'secondary' ? 'Like' : 'Unlike'
        // console.log(e.target.nextElementSibling)
        e.target.nextElementSibling.innerHTML = res.count
    })
}