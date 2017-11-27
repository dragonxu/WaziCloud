let chai = require('chai');
let chaiHttp = require('chai-http');
let should = chai.should();
let baseUrl = require('../config/enviroment').baseUrl;
let domain = require('../config/enviroment').domain;
let socialData = require('../config/sample-data').socials;

chai.use(chaiHttp);


describe('Socials ', () => {

	describe('/domains/{domain}/socials  Get all messages sent', () => {
		it('it should GET all the messages sent', (done) => {
			chai.request(baseUrl)
				.get(`/domains/${domain}/socials`)
				.end((err, res) => {
					res.should.have.status(200);
					res.body.should.be.a('array');
					done();
				});
		});
    });
})