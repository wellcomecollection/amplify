import { Component, OnInit } from '@angular/core';
import {BackendApiService} from '../backend-api.service';

export interface PeriodicElement {
  tag: string;
  code: string;
  subfield: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
];

@Component({
  selector: 'app-worldcat-results',
  templateUrl: './worldcat-results.component.html',
  styleUrls: ['./worldcat-results.component.css']
})
export class WorldcatResultsComponent implements OnInit {

  constructor(
    private backendAPI: BackendApiService
  ) {}

  backend = {
    record_identifier_dict: []
  }

  getVisionOutput() {
    this.backendAPI.getVisionOutputStage1()
    .subscribe(data => {
      this.dataSource = data.worldcat_results;
    })
  }

  displayedColumns: string[] = ['tag', 'code', 'subfield'];
  dataSource = ELEMENT_DATA;

  ngOnInit() {
    this.getVisionOutput();
  }

}
