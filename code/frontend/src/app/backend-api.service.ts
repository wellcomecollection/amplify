import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import {timeout, catchError} from 'rxjs/operators';
import { pythonPost } from './backend.model';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  })
};

// const httpOptionsPost = {
//   headers: new HttpHeaders({
//     'Content-Type': undefined
//   })
// };

const API_URL = 'http://localhost:4204';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {

  constructor(private http: HttpClient) {
  }

  getVisionOutputStage1(frontPage: any): Observable<any> {
    return this.http.post<any>(`${API_URL}/visionStage1`, frontPage)
    .pipe(timeout(86400000));
  }

  getVisionOutputStage2(backendPost: any): Observable<any> {
    return this.http.post<any>(`${API_URL}/visionStage2`, backendPost, httpOptions)
    .pipe(timeout(86400000));
  }

  getVisionOutputStage3(backendPost: any): Observable<any> {
    return this.http.post<any>(`${API_URL}/visionStage3`, backendPost, httpOptions)
    .pipe(timeout(86400000));
  }

  postVisionOutput(backendPost: any): Observable<any> {
    return this.http.post<any>(`${API_URL}/vision_post`, backendPost, httpOptions)
    .pipe(timeout(86400000));
  }

}
