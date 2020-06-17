import { Component, OnInit, Inject} from '@angular/core';
import {BackendApiService} from './backend-api.service';
import { API_URL } from 'src/environments/environment';
import {WorldcatListComponent} from './worldcat-list/worldcat-list.component';
import {interval} from 'rxjs';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';


export interface DialogData {
  tag: string;
  code: string;
  subfield: string;
}

@Component({
  selector: 'app-dialog-component',
  templateUrl: 'app-dialog-component.html',
})

export class DialogOverviewExampleDialogComponent {

  constructor(
    public dialogRef: MatDialogRef<DialogOverviewExampleDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {}

  onNoClick(): void {
    this.dialogRef.close();
  }
}

export interface WorldcatList {
  record_identifier: string;
  title: string;
  worldcat_results: string;
}

export interface WorldcatResults {
  tag: string;
  code: string;
  subfield: string;
}

export interface ABIM {
  author: string;
  date: string;
  link: string;
  title: string;
}

const WORLDCAT_LIST: WorldcatList[] = [];

const WORLDCAT_RESULTS: WorldcatResults[] = [];

const ABIM_LIST: ABIM[] = [];


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit{

  displayedColumns: string[] = [
    'record_identifier', 
    'title',
    'action'];

  displayedColumnsWorldcatResults: string[] = [
    'tag', 
    'code', 
    'subfield', 
    'edit'];

  displayedColumnsABIM: string[] = [
    'author', 
    'date',
    // 'link',
    'title',
  ];

  dataSource = WORLDCAT_LIST;

  dataSourceWorldcatResults = WORLDCAT_RESULTS;
  
  dataSourceABIM = ABIM_LIST;

  title = 'frontend';

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
    library_hub_api_response: [],
    worldcat_results: [],
    status: false,
    libraryhubstatus: false,
    abimstatus: false,
    stage2status: false,
    stage3status: false
  }

  backendPost = {
    image_input: null
  }

  ABIMSearchDict = {
    author: null,
    title: null,
    publisher: null,
    date: null
  }

  ABIMResults = {
    results: []
  }

  tag: string;
  code: string;
  subfield: string;

  constructor(
    private backendAPI: BackendApiService, public dialog: MatDialog,
  ) {}

  selectedFile: File = null;


  editRecord(tag: string, code: string, subfield: string): void {
    
    const dialogRef = this.dialog.open(DialogOverviewExampleDialogComponent, {
      width: '600px',
      data: {tag: tag, code: code, subfield: subfield},
    });
    
    dialogRef.afterClosed().subscribe(result => {
      if (result !== undefined) {
        console.log(result.subfield);
        console.log(this.dataSourceWorldcatResults);
        this.dataSourceWorldcatResults.forEach( (element) => {
          if (element.tag === tag && element.code === code && element.subfield === subfield) {
            element.subfield = result.subfield;
            }
          });
      }
    });
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(DialogOverviewExampleDialogComponent, {
      width: '600px',
      data: {tag: this.tag, code: this.code, subfield: this.subfield}
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      if (result !== undefined) {
        this.tag = result.tag;
        this.code = result.code;
        this.subfield = result.subfield;
        this.addTest(this.tag, this.code, this.subfield);
      }

    });
  }

  addTest(tag: string, code: string, subfield: string) {
    console.log(this.dataSourceWorldcatResults);
    if (tag) {
      this.dataSourceWorldcatResults = this.dataSourceWorldcatResults.concat([{
        tag: tag,
        code: code,
        subfield: subfield
      }]);
    console.log(this.dataSourceWorldcatResults);
    }
  }


  deleteRecord(tag: string, code: string, subfield: string): void {
    console.log(this.dataSourceWorldcatResults);
    this.dataSourceWorldcatResults = this.dataSourceWorldcatResults.filter((value) => {
      return ((value.tag !== tag) || (value.code !== code) || (value.subfield !== subfield))
    });
    console.log(this.dataSourceWorldcatResults);
  }



  onFileSelected(event) {
    this.selectedFile = <File>event.target.files[0];
  }


  onUpload() {
    this.backend.status = true;
    const frontPage = new FormData();
    frontPage.append(
      'image', 
      this.selectedFile, 
      this.selectedFile.name
      )
    this.getVisionOutputStage1(frontPage);
  }


  selectRecord(worldcat_results) {
    this.dataSourceWorldcatResults = worldcat_results;
  }


  libraryHubSearch() {
    this.backend.libraryhubstatus = true;
    this.backendAPI.libraryHubSearch(this.dataSourceWorldcatResults)
    .subscribe(data => {
      this.backend.library_hub_api_response = data.library_hub_api_response;
      this.backend.libraryhubstatus = false;
    })
  }


  getVisionOutputStage1(frontPage) {
    this.backendAPI.getVisionOutputStage1(frontPage)
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
      this.backend.worldcat_results = data.worldcat_results;
      this.dataSource = data.record_identifier_dict;
      this.dataSourceWorldcatResults = data.worldcat_results;
      this.backend.status = false;
    })
  }


  searchABIM(event: any) {
    this.backend.abimstatus = true;
    this.ABIMSearchDict.author = this.backend.author,
    this.ABIMSearchDict.title = this.backend.title,
    this.ABIMSearchDict.publisher = this.backend.publisher,
    this.ABIMSearchDict.date = this.backend.date,
    this.backendAPI.searchABIM(this.ABIMSearchDict)
    .subscribe(data => {
      this.dataSourceABIM = data.abim_results;
      this.backend.record_identifier_dict = data.record_identifier_dict;
      this.dataSource = data.record_identifier_dict;
      this.backend.abimstatus = false;
  })
}


  getVisionOutputStage2() {
    this.backend.stage2status = true;
    this.backendAPI.getVisionOutputStage2(this.backend)
    .subscribe(data => {
      this.backend.detectedSourceLanguage = data.detectedSourceLanguage;
      this.backend.translatedText = data.translatedText;
      this.backend.author = data.author;
      this.backend.title = data.title;
      this.backend.date = data.date;
      this.backend.publisher = data.publisher;
      this.backend.publisher_place = data.publisher_place;
      this.backend.meta_data = data.meta_data;
      this.backend.record_identifier_dict = data.record_identifier_dict;
      this.backend.library_hub_api_response = data.library_hub_api_response;
      this.backend.stage2status = false;
    })
  }


  getVisionOutputStage3() {
    this.backend.stage3status = true;
    this.backendAPI.getVisionOutputStage3(this.backend)
    .subscribe(data => {
      this.backend.author = data.author;
      this.backend.title = data.title;
      this.backend.date = data.date;
      this.backend.publisher = data.publisher;
      this.backend.publisher_place = data.publisher_place;
      this.backend.meta_data = data.meta_data;
      this.backend.record_identifier_dict = data.record_identifier_dict;
      this.backend.library_hub_api_response = data.library_hub_api_response;
      this.backend.stage3status = false;
    })
  }

  postVisionOutput() {
    this.backendAPI.postVisionOutput(this.backendPost)
    .subscribe()
  }


  updateGoogleVisionAPIResponse(event: any) {
    this.backend.google_vision_api_response = event.target.value;
    console.log(this.backend.google_vision_api_response);
  }


  updateTranslatedText(event: any) {
    this.backend.translatedText = event.target.value;
    console.log(this.backend.translatedText);
  }


  updateAuthor(event: any) {
    this.backend.author = event.target.value;
    console.log(this.backend.author);
  }


  updateTitle(event: any) {
    this.backend.title = event.target.value;
    console.log(this.backend.title);
  }


  updateDate(event: any) {
    this.backend.date = event.target.value;
    console.log(this.backend.date);
  }
  

  updatePublisher(event: any) {
    this.backend.publisher = event.target.value;
    console.log(this.backend.publisher);
  }


  updatePublisherPlace(event: any) {
    this.backend.publisher_place = event.target.value;
    console.log(this.backend.publisher_place);
  }

  ngOnInit() {
  }
}
