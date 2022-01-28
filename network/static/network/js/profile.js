console.log('it is working')



function handleFollowBtn(e,id){
    fetch(`/follow/${id}`,{
        method:'PUT',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
    }).then(res => res.json()).then(res => {
        console.log(res);
        let color = res.color
        e.target.classList = 'btn btn-' +color
        e.target.innerHTML = color == 'danger' ? 'Follow' : 'UnFollow'
        document.getElementById('followers_count').innerHTML = res.count
    })
}