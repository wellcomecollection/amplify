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

const API_URL = 'http://localhost:4201';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {

  constructor(private http: HttpClient) {
  }

  getVisionOutput(): Observable<any> {
    return this.http.get<any>(`${API_URL}/vision`, httpOptions)
    .pipe(timeout(86400000));
  }

  postVisionOutput(backendPost: any): Observable<any> {
    return this.http.post<any>(`${API_URL}/vision_post`, backendPost, httpOptions)
    .pipe(timeout(86400000));
  }

}
