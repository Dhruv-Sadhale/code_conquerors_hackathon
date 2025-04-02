
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('background').appendChild(renderer.domElement);

// Create a rotating sphere with lighting and shadows
const geometry = new THREE.SphereGeometry(2, 32, 32, Math.PI / 2, Math.PI * 2, 0, Math.PI);
const material = new THREE.MeshPhongMaterial({ color: 0xff0000, shininess: 50 });
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

const light = new THREE.DirectionalLight(0xffffff, 0.6);
light.position.set(1, 1, 1).normalize();
scene.add(light);

const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

const sphereShadow = new THREE.Mesh(
    new THREE.CircleGeometry(2.5, 32),
    new THREE.ShadowMaterial({ color: 0x000000, opacity: 0.5 })
);
sphereShadow.position.y = -2.001;
scene.add(sphereShadow);

camera.position.z = 5;

let isMouseOver = false;

// Mouse movement interaction
document.addEventListener('mouseenter', () => {
    isMouseOver = true;
});

document.addEventListener('mouseleave', () => {
    isMouseOver = false;
});

// Animation loop
const animate = () => {
    requestAnimationFrame(animate);

    if (isMouseOver) {
        // Rotate the sphere for the background animation
        sphere.rotation.x += 0.005;
        sphere.rotation.y += 0.005;
    }

    renderer.render(scene, camera);
};
animate();

// Animation loop
console.log("here--------------->", questions)
const questionDisplayTime = 2000; // Time each question is displayed in milliseconds
let setNumber = 0;
let questionNumber = 0;
let temp=[];
let count=1;
let parent=[0,0];
let parentfornow=[0,0];
let outer=0;

// Function to add quiz questions to the container
const addQuizQuestion = (question, options, question_id) => {
    const quizContainer = document.getElementById('quiz-container');
    
    // Clear the contents of the quiz container
    quizContainer.innerHTML = '';

    const questionElement = document.createElement('div');
    questionElement.textContent = question;
    quizContainer.appendChild(questionElement);
    count=count+1;
    //console.log("question is:")
    //console.log(question);
    //console.log("in addquizquestion  options:"+options);
    // Add options as buttons
    options.forEach((option, index) => {
        const optionButton = document.createElement('button');
        optionButton.textContent = option;
        //console.log("OPTION:"+option.text)
        optionButton.addEventListener('click', () =>{

         
         handleOptionClick(count, question_id, option)});
        quizContainer.appendChild(optionButton);
    });
};


const recordclub=(dummy)=>{

        // Make an AJAX request to the Django view
        fetch('/api/record_club/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                'dummy': dummy,  // Adjust as needed
               
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Selected option recorded successfully.');
                 window.location.href = '/dashboard/'
            } else {
                console.error('Failed to record selected option:', data.message);
            }
        })
        .catch(error => {
            console.error('Error recording selected option:', error);
        });

    
}
// Function to record the selected option and send it to the backend
const recordSelectedOption = (currentQuestionIndex, option) => {
   // console.log(currentQuestionIndex);
    const selectedOption = option;
    console.log("in recordselectedoption:"+option.club)
    // if(option.club!==null){
    //     recordclub(option.club)
    // }
    if (selectedOption !== null) {
        // Make an AJAX request to the Django view
        fetch('/api/record_response/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                'question_number': currentQuestionIndex,  // Adjust as needed
                'selected_option': selectedOption,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Selected option recorded successfully.');
            } else {
                console.error('Failed to record selected option:', data.message);
            }
        })
        .catch(error => {
            console.error('Error recording selected option:', error);
        });
    }
};


// Handle the option click (e.g., record the answer, move to the next question)
const handleOptionClick = (nextQuestionIndex, currentQuestionIndex, option) => {
    // Record the selected option
   recordSelectedOption(currentQuestionIndex, option);

    // Display the next question or submit button
    displayNextQuestion(nextQuestionIndex);
};



const displayNextQuestion = (nextQuestionIndex) => {
 
    let q="";
    if (nextQuestionIndex <= questions.length) {
        const currentSet = questions;
       // console.log(currentSet)
        console.log("current question no. :"+nextQuestionIndex)
        const currentQuestion = currentSet[nextQuestionIndex-1];
        q=currentQuestion.question;
        let options = new Array(4);
        options[0]=currentQuestion.option1;
        options[1]=currentQuestion.option2;
        options[2]=currentQuestion.option3;
        options[3]=currentQuestion.option4;
        console.log("options are:", options)

        addQuizQuestion(q, options, currentQuestion["qno."]);    
    } else {
        // Display the submit button after all sets are completed
        addSubmitButton();
    }
};

const addSubmitButton = () => {
    const quizContainer = document.getElementById('quiz-container');

    // Clear the contents of the quiz container
    quizContainer.innerHTML = '';

    // Add a submit button
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Prepare Recommendation List';
    submitButton.addEventListener('click', () => handleSubmission());
    quizContainer.appendChild(submitButton);
};



function sendEmail2() {
    return Email.send({
        Host: "smtp.elasticemail.com",
        Username: "dhruv.sadhale@gmail.com",
        Password: "703A64E0DE6E0B9C54CACEDC5B28C8D0A6FD",
        To: "dhruvsadhale.cis@gmail.com",
        From: "dhruv.sadhale@gmail.com",
        Subject: "This is the subject",
        Body: "And this is the body"
    });
}

const handleSubmission = () => {
    console.log("in handlesubmission before recordclub");
    recordclub(0);
    // window.location.href = '/dashboard/';
    
}

const getCSRFToken = () => {
    const csrfCookie = document.cookie
        .split('; ')
        .find(cookie => cookie.startsWith('csrftoken='));

    return csrfCookie ? csrfCookie.split('=')[1] : null;
};

// Initial delay before starting the question cycle
setTimeout(() => displayNextQuestion(1), questionDisplayTime);

// Start the animation loop


animate();