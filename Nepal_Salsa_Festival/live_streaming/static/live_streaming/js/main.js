let localStream;
let remoteStream;
let peerConnection;

let APP_ID = "fa2e87a7a9a14a11b4e663281277a409";

let client;
let channel;

let token = null;
let uid = String(Math.floor(Math.random()*100000));

let queryStrings = window.location.search;
let urlParams = new URLSearchParams(queryStrings);
let roomId = urlParams.get("room");
let broadcaster = urlParams.get("broadcaster");

if(!roomId){
    window.location = "/lobby";
}

const headers = new Headers();
headers.set("Access-Control-Allow-Origin", "*");

const servers = {
  iceServers:[
    {
      urls:['stun:stun1.l.google.com:19302', 'stun:stun2.l.google.com:19302']
    }
  ]
}
const constraints = {
    video: {
      width: {min : 640, ideal:1920, max:1920,
      height: {min : 480, ideal: 1080, max: 1080}
    }
    },
  audio: true
};

async function init(){
  client = await AgoraRTM.createInstance(APP_ID);
  await client.login({uid, token});

  channel = client.createChannel(roomId);
  await channel.join();

  channel.on("MemberJoined", handleUserJoined);
  channel.on("MemberLeft", handleUserLeft);

  client.on("MessageFromPeer", handleMessageFromPeer);

  localStream = await navigator.mediaDevices.getUserMedia(constraints);
  document.getElementById("user-1").srcObject = localStream;
}

async function handleUserJoined(MemberId){
  console.log("A new user joined the channel, ", MemberId);
  createOffer(MemberId);
}

async function handleUserLeft(MemberId){
  console.log("User Left");
  document.getElementById("user-2").style.display = "none";
  document.getElementById("user-1").classList.remove("smallFrame");
}

async function handleMessageFromPeer(message, MemberId){
  message = JSON.parse(message.text);
  if (message.type === "offer"){
    createAnswer(MemberId, message.offer);
  }

  if (message.type === "answer"){
    addAnswer(message.answer);
  }

  if (message.type === "candidate"){
    if(peerConnection){
      peerConnection.addIceCandidate(message.candidate);
    }
  }
}

async function createPeerConnection(MemberId){
  peerConnection = new RTCPeerConnection(servers);

  remoteStream = new MediaStream();
  document.getElementById("user-2").srcObject = remoteStream;
  document.getElementById("user-2").style.display = "block";
  document.getElementById("user-1").classList.add("smallFrame");

  if(!localStream){
    localStream = await navigator.mediaDevices.getUserMedia({video:true, audio: true});
    document.getElementById("user-1").srcObject = localStream;
  }
  localStream.getTracks().forEach(function(track){
    peerConnection.addTrack(track, localStream);
  });

  peerConnection.ontrack = function(event){
    event.streams[0].getTracks().forEach(function(track){
      remoteStream.addTrack(track);
    });
  }

  peerConnection.onicecandidate = async function(event){
    if(event.candidate){
      client.sendMessageToPeer({text: JSON.stringify({"type": "candidate", "candidate":event.candidate})}, MemberId);
    }
  }
}

async function createOffer(MemberId){
  await createPeerConnection(MemberId);

  let offer = await peerConnection.createOffer();
  await peerConnection.setLocalDescription(offer);

  client.sendMessageToPeer({text: JSON.stringify({"type": "offer", "offer":offer})}, MemberId);
}

async function createAnswer(MemberId, offer){
  await createPeerConnection(MemberId);

  await peerConnection.setRemoteDescription(offer);

  let answer = await peerConnection.createAnswer();
  await peerConnection.setLocalDescription(answer);

  client.sendMessageToPeer({text : JSON.stringify({"type": "answer", "answer": answer})}, MemberId);
}

async function addAnswer(answer){
  if (!peerConnection.currentRemoteDescription){
    peerConnection.setRemoteDescription(answer);
  }
}

async function leaveChannel(){
  await channel.leave();
  await client.logout();
}

document.getElementById("leave-btn").addEventListener("click", function(){
  window.location = "/";
});

async function toggleCamera(){
  let videoTrack = localStream.getTracks().find(track => track.kind === "video");
  if(videoTrack.enabled){
    videoTrack.enabled = false;
    document.getElementById("camera-btn").style.backgroundColor = "rgb(255, 80, 80)";
  }else{
    videoTrack.enabled = true;
    document.getElementById("camera-btn").style.backgroundColor = "rgb(179, 102, 249, .9)";
  }
}

async function toggleMic(){
  let audioTrack = localStream.getTracks().find(track => track.kind === 'audio');

  if(audioTrack.enabled){
    audioTrack.enabled = false;
    document.getElementById("mic-btn").style.backgroundColor = "rgb(255, 80, 80)";
  }else{
    audioTrack.enabled = true;
    document.getElementById("mic-btn").style.backgroundColor = "rgb(179, 102, 249, .9)";
  }
}

document.getElementById("camera-btn").addEventListener("click", toggleCamera);

document.getElementById("mic-btn").addEventListener("click", toggleMic);

window.addEventListener("beforeunload", leaveChannel);
init();

/*
let localStream;
let client;
let channel;
let uid = String(Math.floor(Math.random() * 100000));

const APP_ID = "fa2e87a7a9a14a11b4e663281277a409";

async function init() {
    try {
        let queryStrings = window.location.search;
        let urlParams = new URLSearchParams(queryStrings);
        let roomId = urlParams.get("room");
        let broadcaster = urlParams.get("broadcaster");

        if (!roomId && !broadcaster) {
            window.location = "/lobby";
            return;
        }

        client = await AgoraRTM.createInstance(APP_ID);
        await client.login({ uid });

        channel = client.createChannel(roomId);
        await channel.join();

        localStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true// Only need video feed from the broadcaster
        });
        document.getElementById("user-1").srcObject = localStream;
    } catch (error) {
        console.error("Initialization failed:", error);
    }
}

async function leaveChannel() {
    try {
        if (channel) await channel.leave();
        if (client) await client.logout();
        if (localStream) {
            let tracks = localStream.getTracks();
            tracks.forEach(track => track.stop());
        }
    } catch (error) {
        console.error("Cleanup failed:", error);
    }
}

document.getElementById("leave-btn").addEventListener("click", function() {
    leaveChannel().then(() => {
        window.location = "/";
    });
});

window.addEventListener("beforeunload", leaveChannel);
init();
*/

