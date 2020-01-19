import { Component, OnInit } from '@angular/core';
import {BackendApiService} from './backend-api.service';
import { API_URL } from 'src/environments/environment';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit{
  title = 'frontend';
  // author = 'hello';

  backend = {
    google_vision_api_response: [],
    detectedSourceLanguage: [],
    translatedText: [],
    img_loc: [], 
    author: [], 
    title: [], 
    date: [], 
    publisher: [], 
    publisher_place: [],
    meta_data: [],
    record_identifier_dict: [], 
    library_hub_api_response: []
  }

  backendPost = {
    image_input: null
  }

  constructor(
    private backendAPI: BackendApiService
  ) {}

  getVisionOutput() {
    this.backendAPI.getVisionOutput()
    .subscribe(data => {
      this.backend.google_vision_api_response = data.google_vision_api_response;
      this.backend.detectedSourceLanguage = data.detectedSourceLanguage;
      this.backend.translatedText = data.translatedText;
      this.backend.img_loc = data.img_loc;
      this.backend.author = data.author;
      this.backend.title = data.title;
      this.backend.date = data.date;
      this.backend.publisher = data.publisher;
      this.backend.publisher_place = data.publisher_place;
      this.backend.meta_data = data.meta_data;
      this.backend.record_identifier_dict = data.record_identifier_dict;
      this.backend.library_hub_api_response = data.library_hub_api_response;
    })
  }

  postVisionOutput() {
    console.log('posting...')
    // this.backendPost.image_input = image_input
    this.backendAPI.postVisionOutput(this.backendPost)
    .subscribe(
    //   data => {
    // }
    )
  }

  updateGoogleVisionAPIResponse(event: any) {
    this.backend.google_vision_api_response = event.target.value;
  }

  updateAuthor(event: any) {
    this.backend.author = event.target.value;
  }

  updateTitle(event: any) {
    this.backend.title = event.target.value;
  }

  updateDate(event: any) {
    this.backend.date = event.target.value;
  }
  
  updatePublisher(event: any) {
    this.backend.publisher = event.target.value;
  }

  updatePublisherPlace(event: any) {
    this.backend.publisher_place = event.target.value;
  }

  ngOnInit() {
    this.getVisionOutput();
  }
}
