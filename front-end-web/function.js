function dynamicallyLoadScript(url) {
    var script = document.createElement("script"); // create a script DOM node
    script.src = url; // set its src to the provided URL
    document.head.appendChild(script); // add it to the end of the head section of the page (could change 'head' to 'body' to add it to the end of the body section instead)
}
var apigClient;
var name;
var phone;
var res = "";
$(window).load(function () {
    dynamicallyLoadScript("apiGateway-js-sdk/apigClient.js");
    dynamicallyLoadScript("apiGateway-js-sdk/aws-sdk-min.js");
    apigClient = apigClientFactory.newClient();
});
$(".btn").click(function () {
    console.log(apigClient)
    console.log(2);
    name = document.getElementById("name").value;
    phone = document.getElementById("phone").value;
    console.log("name is:", name)
    console.log("phone is:", phone)
    var choices = document.getElementsByTagName('input');
    console.log("choices are: ", choices)
    // loop through all the radio inputs
    for (i = 0; i < choices.length; i++) {
        // if the radio is checked..
        if (choices[i].checked) {
            // add 1 to that choice's score
            if (choices[i].value == 'c1') {
                res+='5';
            }
            if (choices[i].value == 'c2') {
                res+='4';
            }
            if (choices[i].value == 'c3') {
                res+='3';
            }
            if (choices[i].value == 'c4') {
                res+='2';
            }
            if (choices[i].value == 'c5') {
                res+='1';
            }
        }


    }
    console.log("res is:",res)

    // var name = firstName.toLowerCase() + "_" + lastName.toLowerCase(); // 名字传输格式  firstname_lastname
    var body = {
      messages: [
        {
          type: "UserMessage",
          unconstructed: {
            name: name,
            phone: phone,
            rating: res,
          },
        },
      ],
    };
    console.log(body);
    apigClient
      .infoPost({}, body, {})
      .then(function (result) {
        // Add success callback code here
        console.log(result);
        // 是对应的lf里面的response结构
        
      })
      .catch(function (result) {
        // Add error callback code here.
        console.log("failded");
      });
  });

// function tabulateAnswers() {
//     var choices = document.getElementsByTagName('input');
//     console.log("choices are: ", choices)
//     // loop through all the radio inputs
//     var res = [];
//     for (i = 0; i < choices.length; i++) {
//         // if the radio is checked..
//         if (choices[i].checked) {
//             // add 1 to that choice's score
//             if (choices[i].value == 'c1') {
//                 res.append(1);
//             }
//             if (choices[i].value == 'c2') {
//                 res.append(2);
//             }
//             if (choices[i].value == 'c3') {
//                 res.append(3);
//             }
//             if (choices[i].value == 'c4') {
//                 res.append(4);
//             }
//             if (choices[i].value == 'c5') {
//                 res.append(5);
//             }
//             // If you add more choices and outcomes, you must add another if statement below.
//         }


//     }
//     console.log(res)
// }

// function resetAnswer() {
//     var answerbox = document.getElementById('answer');
//     answerbox.innerHTML = "our result will be sent via text message to your phone XD";
// }