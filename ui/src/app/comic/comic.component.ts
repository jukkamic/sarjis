import { Component, Input, Output, OnInit, EventEmitter } from '@angular/core';
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

  ngOnInit(): void {
    this.service.getLatestComic(this.comic.name).subscribe(data=>{
      this.comic = data;
    });
  }

  @Input() comic:any;
  @Output() focusChanged: EventEmitter<any> = new EventEmitter();

  ImageFilePath:string;

  changeFocus() {
    this.focusChanged.emit(this.comic);
  }

  getComic(name:string, id:any) {
    this.service.getComic(name, id).subscribe(data=>{
      this.comic = data;
    });
  }

}
