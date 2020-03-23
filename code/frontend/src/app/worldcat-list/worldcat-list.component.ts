import { Component, OnInit } from '@angular/core';
import {BackendApiService} from '../backend-api.service';
import { AppComponent } from '../app.component';
import { Injectable } from '@angular/core';
import {interval} from 'rxjs';

export interface PeriodicElement {
  record_identifier: string;
  title: string;
  // worldcat_results: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
];

@Component({
  selector: 'app-worldcat-list',
  templateUrl: './worldcat-list.component.html',
  styleUrls: ['./worldcat-list.component.css']
})

@Injectable({
  providedIn: 'root'
})
export class WorldcatListComponent implements OnInit {

  constructor(
    private backendAPI: BackendApiService, 
  ) {}

  backend = {
    record_identifier_dict: []
  }

  // sub = interval(2000)
  // .subscribe((val) => {
  //   console.log('Updating DataSource...');
  //   this.refresh();
  // });

  getRecordIdentifierDict(record_identifier_dict) {
    this.dataSource = record_identifier_dict;
    console.log(this.dataSource);
  }
  
  // refresh(){
  //   this.dataSource = this.backend.record_identifier_dict;
  //   console.log(this.dataSource);
  // }


  // getVisionOutput(frontPage) {
  //   this.backendAPI.getVisionOutputStage1(frontPage)
  //   .subscribe(data => {
  //     this.dataSource = data.record_identifier_dict;
  //   })
  // }

  displayedColumns: string[] = [
    'record_identifier', 
    'title', 
    // 'worldcat_results'
];
  dataSource = ELEMENT_DATA;

  ngOnInit() {
    // this.getVisionOutput();
  }

}
