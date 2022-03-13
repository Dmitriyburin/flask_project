console.log('ок')
let subjects = document.getElementsByClassName("nav-subj");



for (let i = 0 ; i < subjects.length; i++) {
    subjects[i].addEventListener('click', function() {
        for (let j = 0 ; j < subjects.length; j++) {
            subjects[j].classList.remove('active');
        }
        subjects[i].classList.add('active');

    })
    // subjects[i].addEventListener('click', function() {
    //     console.log('привы');
    //     for (let el in subjects) { 
    //         console.log(el.classList.remove('active'))
    //     }
    //     this.classList.add('active');
    // })
}
