const { execFile } = require('child_process');
const { execSync } = require('child_process');

// hash algo for code-server
const argon2 = require('argon2');
const fse = require('fs-extra');
const fs = require('fs');
const fetch = require('node-fetch');

// filebrowser credentials are supposed saved in config/filecreds.json
const creds = require(__dirname + "/../config/filecreds.json");

// change for guaranteed errors
const settings = {
    script: __dirname + "/start_instance.sh",
    template: __dirname + "/../template/index.html",
    user_data: __dirname + "/../data/users/$$user/site/index.html",
    data: __dirname + "/../data/users",
    instances: __dirname + "/../data/users.json",
    login_url: "https://files.by-cy.tech/api/login",
    post_url: "https://files.by-cy.tech/api/users",
    new_user: `{"what":"user","which":[],"data":{"scope":"$$username","locale":"en","viewMode":"mosaic","singleClick":false,"sorting":{"by":"","asc":false},"perm":{"admin":false,"execute":false,"create":true,"rename":true,"modify":true,"delete":true,"share":false,"download":true},"commands":[],"hideDotfiles":false,"dateFormat":false,"username":"$$username","passsword":"","rules":[],"lockPassword":false,"id":0,"password":"$$password"}}`
}

const instances = require(settings.instances);

const default_headers = {
    "authority":"files.by-cy.tech",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "content-type":"application/json",
    "accept":"*/*",
    "origin":"https://files.by-cy.tech",
    "sec-fetch-site":"same-origin",
    "sec-fetch-mode":"cors",
    "sec-fetch-dest":"empty",
    "accept-language":"en-US,en;q=0.9,fr;q=0.8"
}

// Execute any request and returns the response
async function doRequest(url, method = "GET", headers, data = {}) {
    let r = await fetch(url, {
        headers: Object.assign(default_headers, headers),
        method: method,
        redirect: "manual",
        body: method === "POST" ? data : null,
        query: method === "GET" ? data : null
    });
    return r;
}

// Updates user in users.json
async function saveUser(user, password) {
    if (instances.users[user]) {
        console.log("User already exists, overwriting...");
    }
    instances.users[user] = {password: password};
    fs.writeFileSync(settings.instances, JSON.stringify(instances));
}

// Grabs JWT token from filebrowser login
async function doLogin() {
    let r = await doRequest(settings.login_url, "POST", null, JSON.stringify(creds));
    return (await r.text());
}

// Creates user on filebrowser's admin page
async function doCreateUser(jwt, user, password) {
    let r = await doRequest(settings.post_url, "POST", {xauth: jwt, cookie: `auth=${jwt}`}, settings.new_user.replace(/\$\$username/g, user).replace("$$password", password));
    return (await r.text() === "201 Created\n");
}

// Copies template files to new user work directory
async function copyFiles(user) {                       
    let r = true;
    try {
        fse.copySync(settings.template, settings.user_data.replace("$$user", user), overwrite = false);
        await execSync("chmod -R 777 " + settings.data + "/" + user);
    } catch (error) {
        r = false;
    }
    return r;
}

// Runs a docker via the instance script
async function runDocker(user, password) {
    await execFile(settings.script, [user, password], () => {});
}

// Creates a new user docker
async function newInstance(user, password) {
    console.log("Creating user " + user);
    let jwt = await doLogin();
    let r = await doCreateUser(jwt, user, password);
    console.log(r ? "Created user on filebrowser" : "Error creating user on filebrowser");
    password = await argon2.hash(password);
    console.log("Saving user to users list");
    saveUser(user, password);
    console.log("Saved");
    console.log("Copying template files...");
    r = copyFiles(user);
    console.log(r ? "Copied template files" : "Error copying template files");
    console.log("Executing docker creation");
    await runDocker(user, password)
    console.log("Finished.");
}

// Starts an already existing container
async function start(user) {
    if (instances.users[user]) {
        await runDocker(user, instances.users[user].password);
        console.log("Started.");
    } else {
        console.log("User does not exist.");
    }
}

// Stops a running container
async function stop(user) {
    try {
        await execSync("docker stop " + user);
        console.log("Stopped.");
    } catch (error) {
        console.log(error.name);
    }
}

// Prints help
function help() {
    console.log("\nUsage: sudo node users.js <command> [args]\n");
    console.log("\tadd\tusername password\tAdds a new user");
    console.log("\tstart\tusername\t\tStarts container");
    console.log("\tstop\tusername\t\tStops container");

}

// Main
(async () => {
    if (process.argv.length < 4) {
        return help();
    }
    switch (process.argv[2]) {
        case "add":
            if (process.argv.length < 5) return help();
            newInstance(process.argv[3], process.argv[4]);
            break;
        case "start":
            if (process.argv.length < 4) return help();
            start(process.argv[3]);
            break;
        case "stop":
            if (process.argv.length < 4) return help();
            stop(process.argv[3]);
            break;
        default:
            help();
            break;
    }
})();