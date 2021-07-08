import { Component, OnInit } from '@angular/core';
import { ComicService } from 'src/app/comic.service';

@Component({
  selector: 'app-comic',
  templateUrl: './comic.component.html',
  styleUrls: ['./comic.component.css']
})
export class ComicComponent implements OnInit {

  constructor(private service:ComicService) { 
    this.ImageFilePath=this.service.ImageUrl;
  }

  comicList:any=[];
  ImageFilePath:string;

  ngOnInit(): void {
//    this.comic = this.service.getComic(1).subscribe(data=>{
//      this.comic = data;
//    });
    this.service.getAllLatestComics().subscribe(data=>{
      this.comicList = data;
    });

  }

  getComic(name:string, id:any, index:any) {
    this.service.getComic(name, id).subscribe(data=>{
      this.comicList[index] = data;
    });
  }

}
