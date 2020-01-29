import { Component, OnInit } from '@angular/core';
import {BackendApiService} from '../backend-api.service';

// export interface PeriodicElement {
//   name: string;
//   position: number;
//   weight: number;
//   symbol: string;
// }

export interface PeriodicElement {
  record_identifier: string;
  title: string;
}

// const ELEMENT_DATA: PeriodicElement[] = [
//   {position: 1, name: 'Hydrogen', weight: 1.0079, symbol: 'H'},
//   {position: 2, name: 'Helium', weight: 4.0026, symbol: 'He'}
// ];

const ELEMENT_DATA: PeriodicElement[] = [
  {record_identifier: '1', title: 'Hydrogen'},
  {record_identifier: '2', title: 'Helium'}
];

@Component({
  selector: 'app-worldcat-list',
  templateUrl: './worldcat-list.component.html',
  styleUrls: ['./worldcat-list.component.css']
})
export class WorldcatListComponent implements OnInit {

  // constructor() { }

  constructor(
    private backendAPI: BackendApiService
  ) {}

  backend = {
    record_identifier_dict: []
  }

  getVisionOutput() {
    this.backendAPI.getVisionOutput()
    .subscribe(data => {
      // this.backend.record_identifier_dict = data.record_identifier_dict;
      this.dataSource = data.record_identifier_dict;
    })
  }

  // displayedColumns: string[] = ['position', 'name', 'weight', 'symbol'];
  displayedColumns: string[] = ['record_identifier', 'title'];
  dataSource = ELEMENT_DATA;

  ngOnInit() {
    this.getVisionOutput();
  }

}
