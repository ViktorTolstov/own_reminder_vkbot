(function () {
	var url = 'http://127.0.0.1:8080/client_server/';
    $('#submit').on('click', function (e) {
        e.preventDefault();
        let username = $('#username').val();
        let password = $('#password').val();
        let user = {
            "type":"login",
            "username": username,
            "password": password
        };
        checkUser(user);
    })

    async function checkUser(user) {
        const response = await fetch(url, {
            method:"POST",
            body: JSON.stringify(user)
        })
        let groups = await response.json();
        if (groups.correct) {
            //console.log(groups)
        	startAdmin(groups)
        } else {
            $('.error').removeClass('hidden');
        }
    }

    function startAdmin (groups) {
    	$('.wrapper').remove();
        $('#content').html(groups.html);
        addGroups(groups.val);
        $('#request').on('click', async function (e) {
	        e.preventDefault();
	        let contentTextarea = $('#textarea').val()
	        let groupName = $('#list').val()
	        let data = {
                "type":'postNewMessage',
	        	"group":groupName,
	        	"content": contentTextarea 
	        }
        	const response = await fetch(url, {
            	method:"POST",
            	body: JSON.stringify(data)
        	})
        	console.log(await response.json());
    })
    }

    function addGroups(values) {
        console.log(values)
        let list = '<option selected="selected">'+ values[0] +'</option>';
        for (let i = 1; i<values.length; i++) {
            list += '<option>'+ values[i] +'</option>';
        }
        $('#list').html(list);
        
    }
})()

