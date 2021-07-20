import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ComicService {
  readonly APIUrl = environment.api_url;
  readonly ImageUrl = environment.img_url;

  constructor(private http:HttpClient) { }

  getComic(id:any):Observable<any> {
    return this.http.get<any>(this.APIUrl + "comics/id/" + id + "/");
  }

  getLatestComic(name:string | null):Observable<any> {
    return this.http.get<any>(this.APIUrl + "comics/name/" + name + "/").pipe(
      catchError(this.handleError));
  }

  getAllLatestComics():Observable<any[]> {
    return this.http.get<any[]>(this.APIUrl + "comics/")
  }

  getAllNames():Observable<any[]> {
    return this.http.get<any[]>(this.APIUrl + "list-names/");
  }
  
  private handleError(error: HttpErrorResponse) {
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, body was: `, error.error);
    }
    // Return an observable with a user-facing error message.
    return throwError(
      'Something bad happened; please try again later.');
  }

}