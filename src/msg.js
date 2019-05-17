class chat_control {
    constructor() {
        this.msg_list = $('.msg-group');
    }

    send_msg(name, msg) {
        this.msg_list.append(this.get_msg_html(name, msg, 'right'));
        this.scroll_to_bottom(); 
    }

    receive_msg(name, msg) {
        this.msg_list.append(this.get_msg_html(name, msg, 'left'));
        this.scroll_to_bottom(); 
    }

    get_msg_html(name, msg, side) {
        var msg_template = `
            <div class="card">
                 <div class="card-body">
                     <h6 class="card-subtitle mb-2 text-muted text-${side}">${name}</h6>
                     <p class="card-text float-${side}">${msg}</p>
                 </div>
            </div>
            `;
        return msg_template;
    }

    scroll_to_bottom() {
        this.msg_list.scrollTop(this.msg_list[0].scrollHeight);
    }
}

var id_token = '';
// cognito authorization part
// Add the User's Id Token to the Cognito credentials login map.
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-1:977e9af0-7d27-4c82-b672-65da816134f1',
    Logins: {
        'cognito-idp.us-east-1.amazonaws.com/us-east-1_0CFfCfURR' : id_token
    }
});

var apigClient;

AWS.config.credentials.get(function(err) {
  if (err) console.log(err, err.stack); // an error occurred
  else console.log(data); // successful response

    apigClient = apigClientFactory.newClient({
    accessKey: AWS.Credentials.accessKeyId,
    secretKey: AWS.Credentials.secretKey,
    sessionToken: AWS.Credentials.sessionToken,
    region: 'us-east-1' // Replace with the region you deploy
  })
});


function stripEndQuotes(s){
	var t=s.length;
	if (s.charAt(0)=='"') s=s.substring(1,t--);
	if (s.charAt(--t)=='"') s=s.substring(0,t);
	return s;
};

function send_msg_to_aws(parameters){
  body = {'Data': parameters, 'id_token': id_token}
  params = {}
  apigClient.chatbotPost(params, body)
      .then(function(result){
        var value = stripEndQuotes(result.data.body);
        console.log(value.replace(/\"/g, ""))
        chat.receive_msg('Concierge', value.replace(/\"/g, ""))
      }).catch( function(result){
        // Add error callback code here.
        console.log("Error occurred!")
      });
}

var chat = new chat_control();

send_button = $('button') 
input_box = $('#input-box') 

function handle_message(msg) {
    msg = msg.trim()
    msg = msg.replace(/(?:\r\n|\r|\n)/g, '<br>')
    return msg
}

function send_msg() {
    msg = handle_message(input_box.val());
    if (msg != '') {
        send_msg_to_aws(msg)
        chat.send_msg('Me', msg);
        input_box.val('');
    }
}

function box_key_pressing() {
    if ((event.keyCode == 10 || event.keyCode == 13) && event.ctrlKey) {
      send_msg();
    }
    if (event.keyCode == 27) {
        input_box.blur();
    }
}

send_button.on('click', send_msg.bind());
input_box.on('keyup', box_key_pressing.bind());