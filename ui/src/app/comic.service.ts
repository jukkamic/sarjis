import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ComicService {
  readonly APIUrl = "http://localhost:8000/sarjis/";

  constructor(private http:HttpClient) { }

  getComic(name:string, id:any):Observable<any> {
    return this.http.get<any>(this.APIUrl + name + "/" + id);
  }

  getLatestComic(name:string):Observable<any> {
    return this.http.get<any>(this.APIUrl + name);
  }

}

