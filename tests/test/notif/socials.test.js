let chai = require('chai');
let chaiHttp = require('chai-http');
let should = chai.should();
let baseUrl = require('../../config/env').apiUrl;
let socialData = require('./sample-data').socials;
const { getAdminAuth, getNormalAuth} = require('../utils');

chai.use(chaiHttp);

let getSocialMsgs = () => chai.request(baseUrl).get(`/socials`)
let postSocialMsg = (msg) => chai.request(baseUrl).post(`/socials`).send(msg)
let getSocialMsg = (id) => chai.request(baseUrl).get(`/socials/${id}`)
let deleteSocialMsg = (id) => chai.request(baseUrl).delete(`/socials/${id}`)

describe('Socials', () => {
  let withAdmin = null
  let withNormal = null

  //Retrieve the tokens and delete pre-existing sensor
  before(async function () {
    try {
      withAdmin = await getAdminAuth()
      withNormal = await getNormalAuth()
    } catch (err) {
      console.log('error:' + err)
    }
  });
  
  describe('Get all messages sent', () => {
    it('it should GET all the messages sent', async () => {
      let res = await getSocialMsgs().set(withNormal)
      res.should.have.status(200);
      res.body.should.be.a('array');
    });
  });
  describe('post a message to social networks', () => {
    it.skip('it should post a message to twitter', async () => {
      let res = await postSocialMsg(socialData).set(withNormal)
      res.should.have.status(200);
    });
    it('it should fail with bad username', async () => {
      let res = await postSocialMsg({...socialData, username: "5sd54fd5zryetasgsds444444ddd"}).set(withNormal)
      res.should.have.status(400);
    });
  });
  describe('Get one message sent', () => {
    it('it should GET the messages sent', async () => {
      let res = await postSocialMsg(socialData).set(withNormal)
      let res2 = await getSocialMsg(res.text).set(withNormal)
      res2.should.have.status(200);
    });
  });
  describe('Delete one message', () => {
    it('it should DELETE the message', async () => {
      let res = await postSocialMsg(socialData).set(withNormal)
      let res2 = await deleteSocialMsg(res.text).set(withNormal)
      let res3 = await getSocialMsg(res.text).set(withNormal)
      res2.should.have.status(200);
      res3.should.have.status(404);
    });
  });
})
