let subjects = document.getElementsByClassName("nav-subj");
console.log(subjects);

for (let i = 0 ; i < subjects.length; i++) {
    subjects[i].addEventListener('click', function() {
        console.log('привы');
        for (let el in subjects) { 
            console.log(el.classList.remove('active'))
        }
        // this.classList.add('active');
    })

}