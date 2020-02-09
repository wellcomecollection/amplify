import { Component, OnInit } from '@angular/core';
import {BackendApiService} from '../backend-api.service';


export interface PeriodicElement {
  record_identifier: string;
  title: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
];

@Component({
  selector: 'app-worldcat-list',
  templateUrl: './worldcat-list.component.html',
  styleUrls: ['./worldcat-list.component.css']
})
export class WorldcatListComponent implements OnInit {

  constructor(
    private backendAPI: BackendApiService
  ) {}

  backend = {
    record_identifier_dict: []
  }

  getVisionOutput() {
    this.backendAPI.getVisionOutputStage1()
    .subscribe(data => {
      this.dataSource = data.record_identifier_dict;
    })
  }

  displayedColumns: string[] = ['record_identifier', 'title'];
  dataSource = ELEMENT_DATA;

  ngOnInit() {
    this.getVisionOutput();
  }

}
