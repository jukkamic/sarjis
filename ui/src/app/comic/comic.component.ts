import { HttpErrorResponse } from '@angular/common/http';
import { Component, Input, Output, OnInit, EventEmitter } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { throwError } from 'rxjs';
import { ComicService } from 'src/app/comic.service';

@Component({
  selector: 'app-comic',
  templateUrl: './comic.component.html',
  styleUrls: ['./comic.component.css']
})
export class ComicComponent implements OnInit {

  @Input() comic:any;
  @Input() listView:boolean=false;
  ImageFilePath:string;

  constructor(
            private service:ComicService, 
            private route:ActivatedRoute,
            private router:Router
            ) { 
    this.ImageFilePath=this.service.ImageUrl;
  }

  ngOnInit() {
    if( !this.listView )
      this.route.paramMap.subscribe(params=>{
        var id = params.get('id');
        this.service.getComic(id).subscribe(data=>{
          this.comic = data;
        });
      });
  }

  getComic(id:any) {
    this.service.getComic(id).subscribe(data=>{
      this.comic = data;
    });
  }

}
