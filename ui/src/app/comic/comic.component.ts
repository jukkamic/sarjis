import { Component, Input, OnInit } from '@angular/core';
import { ComicService } from 'src/app/comic.service';

@Component({
  selector: 'app-comic',
  templateUrl: './comic.component.html',
  styleUrls: ['./comic.component.css']
})
export class ComicComponent {

  constructor(private service:ComicService) { 
    this.ImageFilePath=this.service.ImageUrl;
  }

  @Input() comic:any;

  ImageFilePath:string;

  getComic(name:string, id:any) {
    this.service.getComic(name, id).subscribe(data=>{
      this.comic = data;
    });
  }

}
