import { Injectable } from '@angular/core';
import sqlite3

@Injectable({
  providedIn: 'root'
})
export class ComicService {

  constructor() { }

  getComic(name:any):
  conn = sqlite3.connect("../../../sarjis.db")


}

