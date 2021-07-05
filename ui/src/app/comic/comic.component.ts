import { Component, OnInit } from '@angular/core';
import { ComicService } from 'src/app/comic.service';

@Component({
  selector: 'app-comic',
  templateUrl: './comic.component.html',
  styleUrls: ['./comic.component.css']
})
export class ComicComponent implements OnInit {

  constructor(private service:ComicService) { }

  comic:any;
  comicList:any=[];

  ngOnInit(): void {
//    this.comic = this.service.getComic(1).subscribe(data=>{
//      this.comic = data;
//    });
    this.service.getComicList().subscribe(data=>{
      this.comicList = data;
    })
  }

}
